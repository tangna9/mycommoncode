#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb
import sys
from conf.mysql import *
__all__ = ['MySQL']
class MySQL(object):
    '''
    MySQL
    '''
    conn = ''
    cursor = ''
    def __init__(self, **MYSQL_DB):

        """MySQL Database initialization """
        try:
            self.conn = MySQLdb.connect(host=MYSQL_DB['host'],
                                        port=MYSQL_DB['port'],
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

    def __del__(self):
        """ Terminate the connection """
        self.cursor.close()
        self.conn.close()


#test
# if __name__ == '__main__':
#
#     mysql = MySQL(**MYSQL_ADSMART)
#     mysql.query('select category_id from ad_provider where shop_id="5384"')
#     result = mysql.showall
#     print len(result)
#     print result
