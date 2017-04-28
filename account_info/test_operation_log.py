# -*- coding: utf-8 -*-
__author__ = 'tangna'
import unittest
import sys
from fg_func.adsmart_common import *
import time
from fg_func.screen import *
reload(sys)
sys.setdefaultencoding('utf8')

current_date = time.strftime('%Y-%m-%d', time.localtime())

class OperationLog(unittest.TestCase):

    def login(func):
        def _login(*args, **kwargs):
            global common
            common = AdSmartCommon(u'firefox')
            common.shop_login()
            func(*args, **kwargs)
            common.logout()
            common.quit()
            return func
        return _login

    @login
    def _get_first_record(self, ur_sign):
        common.goto(adsmart_url.MAIN_URL["operation_log_url"] % (current_date, current_date, 10, 'account'))
        for i in xrange(2, 12):
            if cmp(common.text(AdsmartPagesElements.AccountInfo.column_of_tr % (i, 3)), ur_sign) > 0:
                self.newest_time = common.text(AdsmartPagesElements.AccountInfo.column_of_tr % (i, 1))
                break
        return self.newest_time

    def setUp(self):
        pass

    def test1_login_operation_log(self):
        '''验证登录后，页面上最新一次登录记录和当前时间之差小于60s'''
        self._get_first_record(ur_sign=u"登录")
        print("newest_login_time: %s" % self.newest_time)
        latest_login_time = time.mktime(time.strptime(self.newest_time, '%Y-%m-%d %H:%M:%S '))
        current_time = float(str(time.time()).split('.')[0])
        print("current_time: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)))
        time_diff = current_time - latest_login_time
        self.assertTrue(time_diff < 60,
                        msg='''Not Less! The login_time is:{},
                        current_time is:{}'''.format(latest_login_time, current_time))

    def test2_logout_operation_log(self):
        '''验证登录后，页面上最新一次退出记录和当前时间之差小于60s'''
        self._get_first_record(ur_sign=u"退出")
        print("newest_logout_time: %s" % self.newest_time)
        latest_login_time = time.mktime(time.strptime(self.newest_time, '%Y-%m-%d %H:%M:%S '))
        current_time = float(str(time.time()).split('.')[0])
        print("current_time: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)))
        time_diff = current_time - latest_login_time
        self.assertTrue(time_diff < 60,
                        msg='''Not Less! The logout_time is:{},
                        current_time is:{}'''.format(latest_login_time, current_time))

    def tearDown(self):
        common.quit()
        pass

if __name__ == "__main__":
    unittest.main()
