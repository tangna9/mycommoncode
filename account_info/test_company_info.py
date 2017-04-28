# -*- coding: utf-8 -*-
__author__ = 'tangna'
import unittest
import sys
from fg_func.adsmart_common import *
from fg_func.Mysql import MySQL
from fg_func.screen import *
import time
from conf.mysql import *
reload(sys)
sys.setdefaultencoding('utf8')

class CompanyInfo(unittest.TestCase):

    def setUp(self):
        self.common = AdSmartCommon(u'firefox')
        self.common.shop_login()
        self.common.goto(adsmart_url.MAIN_URL['company_info_url'])
        print adsmart_url.MAIN_URL['company_info_url']
        self.__db = MySQL(**MYSQL_ADSMART)

    #\x9a 实际是：的某个编码，试了直接给冒号encode（utf-8）却得不到
    def __str_format(self, my_str):
        return my_str.encode("utf-8").split("\x9a")[1].strip()

    def __query_sql(self, sql):
        self.__db.execute(sql)
        return self.__db.show_all

    def __get_cate_info_from_db(self):
        cate_name = []
        category_id = self.__query_sql(sql='select category_id from ad_provider where shop_id=%s' %c.LOGIN_INFO['SHOPID'])
        last_id = category_id[0][0]
        while True:
            result = self.__query_sql(sql='SELECT name, pid from category where id = %s and status = 1' %last_id)
            cate_name_current, pid = result[0][0], result[0][1]
            cate_name.append(cate_name_current)
            last_id = pid
            if pid == 0:
                break
        return cate_name

    def test1_username_in_company_info(self):
        '''验证商家信息中的登录名正确'''
        uname_on_page = self.__str_format(self.common.text(AdsmartPagesElements.AccountInfo.company_info_uname))
        self.assertEquals(uname_on_page,
                          c.LOGIN_INFO['SHOP_USERNAME'],
                          msg='''Not equal! The username on the page is:{},
                          the one used to log in is:{}'''.format(uname_on_page, c.LOGIN_INFO['SHOP_USERNAME']))

    def test2_company_id_in_company_info(self):
        '''验证商家信息中的商品编号正确'''
        company_id_on_page = self.__str_format(self.common.text(AdsmartPagesElements.AccountInfo.company_info_id))
        self.assertEqual(company_id_on_page,
                         c.LOGIN_INFO['SHOPID'],
                         msg='''Not equal! The company_id on the page is:{},
                         the one used to log in is:{}'''.format(company_id_on_page, c.LOGIN_INFO['SHOPID']))

    def test3_company_category_in_company_info(self):
        '''验证商家信息中的主营商品正确'''
        #status是0的好像也不显示，比如shop_id：18121
        company_category_on_page = self.__str_format(self.common.text(AdsmartPagesElements.AccountInfo.company_info_category))
        #print company_category_on_page
        cate_info_of_db = self.__get_cate_info_from_db()
        if len(cate_info_of_db[:-1]) > 1:
            cate_info_of_db_format = (">{} > {}").format(cate_info_of_db[1], cate_info_of_db[0])
        else:
            cate_info_of_db_format = (">{}").format(cate_info_of_db[0])
        #print cate_info_of_db_format
        self.assertEqual(company_category_on_page,
                         cate_info_of_db_format,
                         msg='''Not equal! The company_category on the page is:{},
                         the one in db is:{}'''.format(company_category_on_page, cate_info_of_db_format))

    def test4_modify_company_name(self):
        '''验证修改商家信息的公司名称，修改后和数据库一致'''
        old_company_name = self.common.get_attribute(AdsmartPagesElements.AccountInfo.company_info_name, 'value').split('_')[0]
        modified_company_name = old_company_name+'_'+time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.common.send_keys(AdsmartPagesElements.AccountInfo.company_info_name, modified_company_name)
        self.common.click(AdsmartPagesElements.AccountInfo.confirm_button)
        company_name_db = self.__query_sql("select company_name from ad_provider where shop_id = %s" % c.LOGIN_INFO['SHOPID'])[0][0]
        self.assertEqual(modified_company_name,
                         company_name_db,
                         msg='''Not equal! The modified_company_name is:{},
                         the one in db is:{}'''.format(modified_company_name, company_name_db))

    def test5_modify_company_tel(self):
        '''验证修改商家信息的电话号码，修改后和数据库一致'''
        #old_tel = self.common.get_attribute(AccountInfo.company_info_phone, 'value')
        modified_tel = str(time.time()).split(".")[0]+"1"
        print modified_tel
        self.common.send_keys(AdsmartPagesElements.AccountInfo.company_info_phone, modified_tel)
        self.common.click(AdsmartPagesElements.AccountInfo.confirm_button)
        tel_db = self.__query_sql("SELECT phone from ad_user where id = \
                                  (select ad_user_id from ad_provider where shop_id = %s)" % c.LOGIN_INFO['SHOPID'])[0][0]
        self.assertEqual(modified_tel,
                         tel_db,
                         msg='''Not equal! The modified tel is:{},
                         the one in db is:{}'''.format(modified_tel, tel_db))

    def tearDown(self):
        self.common.quit()

if __name__ == "__main__":
    unittest.main()