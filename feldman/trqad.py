from __future__ import print_function, division, absolute_import


from feldman.config import Config

from sqlalchemy.sql import column, and_, or_
import datetime as dt
from os.path import join as pjoin
import os
from feldman.arraymanagementclient import ArrayManagementClient



class TRQAD(ArrayManagementClient):

    def __init__(self, path=None):
        self.init__ = super(TRQAD, self).__init__()

    @property
    def gics(self):

        #empty select reads all
        return self.aclient['/gicsec'].select()



    def find_entity(self,entity=None):
        secmstrx_df = self.aclient['/sec.fsql']
        if not entity:
            return secmstrx_df
        else:
            if isinstance(entity,int):
                seccode_match = secmstrx_df.select(secmstrx_df.seccode==entity)
                return seccode_match
            else:
                name_match = secmstrx_df.select(secmstrx_df.name.like('%%%s%%' % str(entity) ))
                return name_match

    def get_giccodes(self,name):
        codes = self.aclient['/gicsec'].select(where=[('INDUSTRY', name)])
        return codes

    def ws_meas(self,universe, metrics,dt_list,freq='Q'):
        ws_data = self.aclient['/WSNDATA/wsndata.bsqlspec'].select(
                    seccode=universe,
                    item=metrics,
                    freq=freq,
                    fdate=[dt_list[0], dt_list[1]]
                    )
        return ws_data

    def ds_meas_ohlc(self,universe,dt_list):
        ds_data = self.aclient['/DataStream/ohlcview.sqlspec'].select(
                    seccode=universe,
                    marketdate=[dt_list[0],
                                dt_list[1]]
                    )

        return ds_data

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
        """

        declares, sets, fields, comments, output = self.tr_sql_parser(file_input)
        fsql_output = pjoin(self.basedir,file_output)
        with open(fsql_output,'w') as f:
            for line in output:
                print(line,file=f)
            print('---',file=f)
            field_line =', '.join(fields)
            print(field_line,file=f)


