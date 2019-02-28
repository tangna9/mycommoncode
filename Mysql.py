#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author:TangNa

import MySQLdb
import sys
from conf.mysql import *
__all__ = ['MySQL']
class MySQL(object):
    '''
    MySQL
    '''

    def __init__(self, **MYSQL_DB):

        """MySQL Database initialization """
        try:
            self.conn = MySQLdb.connect(host=MYSQL_DB['host'],
                                        port=int(MYSQL_DB['port']),
                                        user=MYSQL_DB['user'],
                                        passwd=MYSQL_DB['password'],
                                        db=MYSQL_DB['db'],
                                        charset=MYSQL_DB['charset'])
        except MySQLdb.Error, e:
            errormsg = 'Cannot connect to server\nERROR (%s): %s' %(e.args[0],e.args[1])
            print errormsg
            sys.exit()

        self.cursor = self.conn.cursor()

    def execute(self, sql):
        """  Execute SQL statement """
        self.cursor.execute(sql)

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    @property
    def show_one(self):
        """ Return the result after executing SQL statement """
        return self.cursor.fetchone()

    @property
    def show_all(self):
        """ Return the result after executing SQL statement """
        return self.cursor.fetchall()

    def query(self, sql):
        """  Execute SQL statement """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def __del__(self):
        """ Terminate the connection """
        self.conn.close()
        self.cursor.close()

#test
if __name__ == '__main__':

    mysqltest = MySQL(**MYSQL_DB)
    result = mysqltest.query('select * from hug_parameter limit 1')
    print len(result)
    print result
