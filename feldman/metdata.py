from __future__ import print_function, division, absolute_import


from feldman.config import Config

from sqlalchemy.sql import column, and_, or_
import datetime as dt
from os.path import join as pjoin
import os
from feldman.arraymanagementclient import ArrayManagementClient

class TRMETA(ArrayManagementClient):

    def __init__(self, path=None):
        super(TRMETA, self).__init__()

    @property
    def gics(self):

        #empty select reads all
        return self.aclient['/gicsec'].select()

    def find_entity_id(self,entity=None,origin='us'):
        """
        :type entity: string
        :param entity: name to match on

        :type origin: string
        :param origin: origin to search for: us or non-us

        :rtype: `pandas.DataFrame`
        :return: DataFrame of match

        """

        if origin == 'us':
            secmstrx_df = self.aclient['/SECCODES/sec.fsql']
        else:
            secmstrx_df = self.aclient['/SECCODES/gsec.fsql']

        if isinstance(entity,int):
            seccode_match = secmstrx_df.select(secmstrx_df.seccode==entity)
            return seccode_match
        else:
            raise Exception("ValueError: Searching by integer")

    def find_entity_name(self,entity=None,origin='us'):
        """
        :type entity: int
        :param entity: seccode to match on

        :type origin: string
        :param origin: origin to search for: us or non-us

        :rtype: `pandas.DataFrame`
        :return: DataFrame of match

        """

        if origin == 'us':
            secmstrx_df = self.aclient['/SECCODES/sec.fsql']
        else:
            secmstrx_df = self.aclient['/SECCODES/gsec.fsql']

        if isinstance(entity,str):
            name_match = secmstrx_df.select(secmstrx_df.name.like('%%%s%%' % str(entity) ))
            return name_match
        else:
            raise Exception("ValueError: Searching by String")

    def get_giccodes(self,name):
        codes = self.aclient['/gicsec'].select(where=[('INDUSTRY', name)])
        return codes


    def get_rkd_items(self):
        '''retrieve rkd items dataframe and add enumeration'''
        index_name = 'COA'
        items = self.aclient['/RKD/items.sql'].select()
        for i in items[index_name]:
            thisitem = items[items[index_name]==i]
            setattr(items,i,thisitem)
        return items

    def get_ibes_measures(self):
        index_name = 'Measure'
        items = self.aclient['/IBES/items.sql'].select()
        for i in items[index_name]:
            thisitem = items[items[index_name]==i]
            setattr(items,i,thisitem)
        return items

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
        ---
        seccode, name

        DEFAULT BEHAVIOR IS WRITING OVER FILE
        """

        declares, sets, fields, comments, output = self.tr_sql_parser(file_input)
        fsql_output = pjoin(self.basedir,file_output)
        with open(fsql_output,'w') as f:
            for line in output:
                print(line,file=f)
            print('---',file=f)
            field_line =', '.join(fields)
            print(field_line,file=f)
