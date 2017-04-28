#encoding:utf8
import sys
sys.path.append("D:\\ad_ui_test")
from fg_func.adangdang_common import *
import unittest
from conf import adangdang_url as adang
import logging
import logging.config

reload(sys)
sys.setdefaultencoding('utf8')

class CategoryAd(unittest.TestCase):

    def setUp(self):
        self.common = AddangdangCommon('firefox')
        logging.config.fileConfig("D:\\ad_ui_test\\conf\logging.conf")
        self.logger = logging.getLogger("adang")

    def testcase11_category_ad_nbook(self):
        '''验证百货分类品页左侧单品广告点击日志，曝光日志，request日志，ad_log_cpc数据'''

        url = "http://category.dangdang.com/cid4001077.html"
        self.logger.info("go to %s" % url)

    def tearDown(self):
        print u". 退出浏览器"
        self.common.quit()

if __name__ == '__main__':
    suit = unittest.defaultTestLoader.loadTestsFromTestCase(CategoryAd)
    unittest.TextTestRunner().run(suit)




