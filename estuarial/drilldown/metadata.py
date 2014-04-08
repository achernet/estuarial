from __future__ import print_function, division, absolute_import

import os
import datetime as dt
from os.path import join as pjoin
from sqlalchemy.sql import column, and_, or_
from estuarial.util.config.config import Config
from estuarial.array.arraymanagementclient import ArrayManagementClient
from estuarial.util.dateparsing import parsedate, end_of_month
from estuarial.util.munging import lower_columns


class TRMETA(ArrayManagementClient):

    def __init__(self, path=None):
        super(TRMETA, self).__init__()

    @property
    def gicidx(self):
        arr = self.aclient['/METADATA/gic_indices.yaml']
        return arr.select(query_filter=None)


    def gics(self,date,idx='LS&PCOMP'):
        """
        Function to return gics codes for a particular month for a particular index

        :type date: string/datetime
        :param date: end of month for a given month e.g. 2014-01-31

        :type idx: string
        :param idx: valid index parameter (default LS&PCOMP) for valid indices, check meta.gicidx

        :rtype: `pandas.DataFrame`
        :return: DataFrame of GICs codes for a particular month

        """

        arr = self.aclient['/METADATA/gic_date_select.yaml']
        date = parsedate([date])[0]
        if not end_of_month(date):
            raise Exception("{}: is not end of the month".format(str(date)))

        data = arr.select(
                and_(arr.indexlistmnem==idx,
                     arr.date_ == date,
                     )
                )
        return data

    def find_entity_id(self, entity=None, origin='us'):
        """
        :type entity: string
        :param entity: name to match on

        :type origin: string
        :param origin: origin to search for: us or non-us

        :rtype: `pandas.DataFrame`
        :return: DataFrame of match
        """

        if origin == 'us':
            secmstrx_df = self.aclient['/SECCODES/sec.yaml']
        else:
            secmstrx_df = self.aclient['/SECCODES/gsec.yaml']

        if isinstance(entity, int):
            seccode_match = secmstrx_df.select(secmstrx_df.seccode==entity)
            return seccode_match
        else:
            raise Exception("ValueError: Searching by integer")

    def find_entity_name(self, entity=None, origin='us'):
        """
        :type entity: int
        :param entity: seccode to match on

        :type origin: string
        :param origin: origin to search for: us or non-us

        :rtype: `pandas.DataFrame`
        :return: DataFrame of match
        """

        if origin == 'us':
            secmstrx_df = self.aclient['/SECCODES/sec.yaml']
        else:
            secmstrx_df = self.aclient['/SECCODES/gsec.yaml']

        if isinstance(entity, str):
            name_match = secmstrx_df.select(
                secmstrx_df.name.like('%%%s%%' % str(entity)))
            return name_match
        else:
            raise Exception("ValueError: Searching by String")

    def get_giccodes(self,name):
        codes = self.aclient['/gicsec'].select(where=[('INDUSTRY', name)])
        return codes

    def get_rkd_items(self):
        '''retrieve rkd items dataframe and add enumeration'''
        index_name = 'COA'
        items = self.aclient['/RKD/items.yaml'].select()
        for i in items[index_name]:
            thisitem = items[items[index_name]==i]
            setattr(items,i,thisitem)
        return items

    def get_ibes_measures(self):
        index_name = 'Measure'
        items = self.aclient['/IBES/items.yaml'].select()
        for i in items[index_name]:
            thisitem = items[items[index_name]==i]
            setattr(items,i,thisitem)
        return items

    def to_rkdcode(self, seccodes=None, tickers=None, CntryCode='USA'):
        """
        :type seccodes: list
        :param seccodes: list of seccodes

        :type origin: string
        :param origin: origin to search for: us or non-us

        :rtype: `pandas.DataFrame`
        :return: DataFrame of match
        """

        url = '/ENTITYMANAGEMENT/seccode_to_rkd_code.yaml'
        arr = self.aclient[url]

        if tickers is None:
            data = arr.select(
                and_(arr.seccode.in_(seccodes),
                     arr.cntrycode==CntryCode),
                    )

        if seccodes is None:
            data = arr.select(
                and_(arr.ticker.in_(tickers),
                     arr.cntrycode==CntryCode),
                    )
        data = lower_columns(data)
        return data


    def tr_sql_parser(file_input):
        """
        Parses SQL statement into numerous lists
        remove lines with declare, set, --, ORDERBY

        :type file_input: string
        :param file_input: Input file TR SQL query example

        :rtype: list of strings
        :return: A bunch of lists
        """

        declares = []
        sets = []
        wheres = []
        comments = []
        output = []
        with open(file_input, "r") as f:
            data = f.read()

        for line in data.split('\n'):
            if line.startswith('DECLARE'):
                declares.append(line)
            elif line.startswith('SET'):
                sets.append(line)
            elif line.startswith('WHERE'):
                wheres.append(line)
            elif line.startswith('--'):
                comments.append(line)
            else:
                output.append(line)
        fields = [field.split('@')[1] for field in wheres]
        return declares, sets, fields, comments, output

    def to_fsql(self,file_input, file_output):
        """
        Convert SQL to ArrayManagement SQL.

        :type file_input: string
        :param file_input: Input file TR SQL query example

        select * from secmstrx
        +++
        seccode, name

        DEFAULT BEHAVIOR IS WRITING OVER FILE
        """

        declares, sets, fields, comments, output = (
            self.tr_sql_parser(file_input))

        fsql_output = pjoin(self.basedir,file_output)
        with open(fsql_output,'w') as f:
            for line in output:
                print(line,file=f)
            print('+++',file=f)
            field_line =', '.join(fields)
            print(field_line,file=f)
