#!/usr/bin/env python
#encoding:utf8
'''
Project : AD_UI_test
Version : v0.1
Author : tangna@dangdang.com, xiyucheng@dangdang.com, duyaming@dangdang.com
Date : 2016-03-14
Note :本程序UI测试的基础类，提供关于selenium的各种方法，不可单独执行
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from conf.pages_elements import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime

class BaseFunc(object):

    #初始化浏览器，获得driver
    def __init__(self, browser_type='Firefox'):
        if browser_type in ['IE', 'ie', 'Ie']:
            self.driver = webdriver.IE()
        elif browser_type in ['Chrome', 'CHROME', 'chrome']:
            self.driver = webdriver.Chrome()
        elif browser_type in ['Firefox', 'FIREFOX', 'FireFox', 'firefox']:
            self.driver = webdriver.Firefox()
            #self.driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    #等待页面元素加载
    def wait_for_element_load(self, element, timeout=45):
        locator = self.get_element_locator(element)
        element = element.split("->")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
                )
        except Exception, e:
            print element, "Element not found"
        return element

    def get_element_locator(self,element):
        element_locator = ()
        element = element.split("->")
        if element[0] in ['id', 'ID', 'Id']:
            element_locator = (By.ID, element[-1])
        elif element[0] in ['xpath', 'XPATH', 'Xpath']:
            element_locator = (By.XPATH, element[-1])
        return element_locator

    def find_element(self, element, timeout=30):
        element = self.wait_for_element_load(element, timeout)
        element = self.driver.find_element(by=element[0], value=element[-1])
        return element

    #得到元素的list
    def find_elements(self, element, timeout=30):
        element = self.wait_for_element_load(element, timeout)
        element_list = self.driver.find_elements(by=element[0], value=element[-1])
        return element_list

    #等待元素消失
    def wait_for_element_invisible(self, element, timeout=30):
        element = element.split("->")
        if element[0] in ['id', 'ID', 'Id']:
            locator = (By.ID, element[-1])
        elif element[0] in ['xpath', 'XPATH', 'Xpath']:
            locator = (By.XPATH, element[-1])
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
                )
        except Exception, e:
            print element, "Element did not disappear in %d seconds" % timeout

    #判断页面元素是否存在
    def is_element_present(self, element):
        element = element.split("->")
        try:
            self.driver.find_element(by=element[0], value=element[-1])
        except NoSuchElementException, e:
            return False
        return True

    #打开url
    def goto(self, url):
        try:
            goto = self.driver.get(url)
        except Exception, urlnotreached:
            print "url not reached"
        return goto

    def switch_to_frame(self, frame_name):
        self.driver.switch_to.frame(frame_name)

    def switch_back(self):
        self.driver.switch_to.default_content()

    #点击某页面元素
    def click(self, element):
        element = self.wait_for_element_load(element)
        self.driver.find_element(by=element[0], value=element[-1]).click()

    #清空页面元素的内容
    def clear(self, element):
        element = self.wait_for_element_load(element)
        self.driver.find_element(by=element[0], value=element[-1]).clear()

    #清空页面元素内容并设置值
    def send_keys(self, element, key):
        element = self.wait_for_element_load(element)
        self.driver.find_element(by=element[0], value=element[-1]).clear()
        self.driver.find_element(by=element[0], value=element[-1]).send_keys(key)

    #获取页面元素属性值
    def get_attribute(self, element, name):
        element = self.wait_for_element_load(element)
        return self.driver.find_element(by=element[0], value=element[-1]).get_attribute(name)

    #去除对应页面元素的只读属性
    #如时间控件对应的input的只读属性
    def remove_readonly(self, element):
        element = self.wait_for_element_load(element)
        self.driver.find_element(by=element[0], value=element[-1])
        self.driver.execute_script("var setDate=document.getElementById(\'"+element[-1]+"\');setDate.removeAttribute('readonly');")


    #获得页面元素的text
    def text(self, element):
        element = self.wait_for_element_load(element)
        return self.driver.find_element(by=element[0], value=element[-1]).text

    #取得表格的列数
    def get_table_column_num(self, element):
        if '->' in element:
            element = element.split("->")
        else:
            element = element
        th_element = self.driver.find_elements(by=element[0], value=element[-1]+str('/.//tr[0]/td'))
        column_count = 0
        for i in th_element:
            if not u'display: none' in i.get_attribute('style'):
                column_count += 1
        return column_count

    #取得表格的行数
    def get_table_row_num(self, element):
        if '->' in element:
            element = element.split("->")
        else:
            element = element
        tr_element = self.driver.find_elements(by=element[0], value=element[-1]+str('/tbody/tr'))
        return len(tr_element)

    #取得列表的列数
    def get_list_column_num(self, element):
        if '->' in element:
            element = element.split("->")
        else:
            element = element
        li_element = self.driver.find_elements(by=element[0], value=element[-1]+str('/ul[1]/li'))
        column_count = 0
        for i in li_element:
            if i.text:
                column_count += 1
        return column_count

    #取得列表的行数
    def get_list_row_num(self, element):
        if '->' in element:
            element = element.split("->")
        else:
            element = element
        ul_element = self.driver.find_elements(by=element[0], value=element[-1]+str('/.//ul'))
        return len(ul_element)

    #退出浏览器
    def quit(self):
        self.driver.quit()

    #提交表单
    def submit(self, element):
        element = self.wait_for_element_load(element)
        self.driver.find_element(by=element[0], value=element[-1]).click()

    #以列表嵌套方式返回页面中列表中的行数据，默认列表共7列，返回当前页面所有行,通过index取对应的行
    #element格式参考："xpath->.//*[@id='form_ads']"
    def list_row_content(self, element):
        element = self.wait_for_element_load(element)
        column_num = self.get_list_column_num(element)
        if column_num == 0:
            raise "列表中没有数据"
        row = []
        all_rows = []
        count = 0
        all_li = self.driver.find_elements(by=element[0], value=element[-1]+str('/.//li'))
        try:
            for i in all_li:
                if i.text:
                    row.append(i.text)
                    count += 1
                if count % column_num == 0 and row:
                    all_rows.append(row)
                    row = []
        except Exception,e:
            print "无法取到列表中数据"
        return all_rows

    #以列表嵌套方式返回页面中列表中的列数据，默认列表共7列，共10行，返回所有列，通过index取对应列
    #element格式参考："xpath->.//*[@id='form_ads']"
    def list_column_content(self, element):
        all_column = []
        all_rows = self.list_row_content(element)
        try:
            all_column = [[r[col] for r in all_rows] for col in range(len(all_rows[0]))]
        except Exception, e:
            print "无法取到表格数据"
        return all_column

    #以列表嵌套方式返回页面中table中的行数据，默认列数为12列（有些列隐藏了，其对应text为空，在这里过滤了）
    #返回当前页面所有行，通过index取对应列,"xpath->//table[@class='table']"
    def table_row_content(self, element):
        element = self.wait_for_element_load(element)
        column_num = self.get_table_column_num(element)
        row = []
        all_rows = []
        count = 0
        all_li = self.driver.find_elements(by=element[0], value=element[-1]+str('/.//td'))
        try:
            for i in all_li:
                if i.text:
                    row.append(i.text)
                    count += 1
                if count % column_num == 0 and row:
                    all_rows.append(row)
                    row = []
        except Exception, e:
            print "无法取到表格数据"
        return all_rows

    #以列表嵌套方式返回页面中表格的列数据，默认列表共12列，共15行，返回所有列，通过index取对应列
    #element格式参考："xpath->//table[@class='table']"
    def table_column_content(self, element):
        all_column = []
        all_rows = self.table_row_content(element)
        try:
            all_column = [[r[col] for r in all_rows] for col in range(len(all_rows[0]))]
        except Exception, e:
            print "无法取到表格数据"
        return all_column

    # 选择下拉列表中的一项，choice可以是下拉列表项的text也可以是数字索引
    # 示例：action.select("xpath->.//*[@id='pos_id']/option", u"回头客推广位")
    def select(self, element, choice):
        element = self.wait_for_element_load(element)
        all_options = self.driver.find_elements(by=element[0], value=element[-1])
        chosen = None
        for i in xrange(len(all_options)):
            if choice == all_options[i].text:
                chosen = i
            elif choice == i:
                chosen = i
        try:
            all_options[chosen].click()
        except Exception, e:
            print "没有该选项"

    #取得页面中的checkbox，返回的是所有的checkbox，要使用其中一个，需要使用[i]的方式
    def get_checkbox(self):
        try:
            checkbox = self.driver.find_elements_by_css_selector('input[type=checkbox]')
        except Exception,e:
            print "该页面没有checkbox"
        return checkbox

    # 从list当去取得a链接，chice为a链接的text
    # //li//a[text()='推广'] example:action.click_a_in_list("xpath->//li//a", "推广")
    def get_a_in_list(self, element, choice):
        element = self.wait_for_element_load(element)
        all_a = self.driver.find_elements(by=element[0], value=element[-1]+str('[text()="%s"]' %choice))
        return all_a
        #random.choice(all_a).click()

    #取得提示框的文本
    def get_text_from_alert(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
        except Exception,e:
            print "没有弹出窗口"
        return alert.text

    def accept_alert(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            alert.accept()
        except:
            print("no alert")

    def dismiss_alert(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            alert.dismiss()
        except:
            print("no alert")

    def wait_for_alert_close(self, timeout=30):
        WebDriverWait(self.driver, timeout).until_not(EC.alert_is_present())

    def get_page_number(self, element):
        pass

    #windows_name为打开窗口的title
    def switch_to_windows(self, windows_name):
        handles = self.driver.window_handles
        for i in handles:
            self.driver.switch_to_window(i)
            if self.driver.title == windows_name:
                break

    #截图
    def screen_shot(self, url, filename):
        self.driver.get(url)
        self.driver.save_screenshot(filename)
        self.driver.quit()

    #最大化浏览器窗口
    def max_window(self):
        self.driver.maximize_window()


    #ctrl+a全选
    def ctrl_a(self, element):
        element = self.wait_for_element_load(element)
        self.driver.find_element(by=element[0], value=element[-1]).send_keys(Keys.CONTROL, 'a')
        return element

    #ctrl+a全选后点击键盘删除键
    def ctrl_a_delete(self, element):
        element = self.ctrl_a(element)
        self.driver.find_element(by=element[0], value=element[-1]).send_keys(Keys.DELETE)

    #回车
    def click_enter(self, element):
        element = self.ctrl_a(element)
        self.driver.find_element(by=element[0], value=element[-1]).send_keys(Keys.ENTER)

    #鼠标hover
    def mouse_hover(self, element):
        element = self.wait_for_element_load(element)
        a = self.driver.find_element(by=element[0], value=element[-1])
        ActionChains(self.driver).move_to_element(a).perform()

    #移动页面滚动条, 参数为移动多少像素，如scroll_page_to_bottom("200")滚动条向下移动200像素，默认移动至底部
    #x左右移动，可为负数字符串， y上下移动
    def scroll_page(self, x="0", y="document.body.scrollHeight"):
        self.driver.execute_script("window.scrollTo("+x+", "+y+");")

    #移动页面滚动条直到看到某页面元素
    def scroll_page_till_see(self, element):
        element = self.wait_for_element_load(element)
        element = self.driver.find_element(by=element[0], value=element[-1])
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_till_see_by_id(self, element_id):
        self.wait_for_element_load(element_id)
        element_id = element_id.split("->")[-1]
        self.driver.execute_script('document.getElementById("%s").scrollIntoView(true);' % element_id)

    #获得当前的url
    def get_current_url(self):
        return self.driver.current_url

    #获得cookie信息
    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return cookies

    #删除所有cookie
    def delete_cookies(self):
        self.driver.delete_all_cookies()

    #删除指定cookie
    def delete_cookie_by_name(self, name):
        self.driver.delete_cookie(name)
    # dxh：定位当前窗口句柄
    def current_window(self):
        current_window=self.driver.current_window_handle
        return current_window
    #dxh：获取所有窗口句柄
    def all_windows(self):
        all_windows=self.driver.window_handles
        return all_windows
    #dxh:获取给定句柄的浏览器窗口
    def switch_to_new_window(self, windows_haddle):
        self.driver.switch_to_window(windows_haddle)
    #dxh：关闭浏览器窗口
    def close_window(self):
        self.driver.close()
    #dxh:返回上个月第一天和最后一天
    def get_mon(self,date):
        firstday=str((date.replace(day=1)-datetime.timedelta(1)).replace(day=1))

        lastday=str(date.replace(day=1)-datetime.timedelta(1))
        return firstday,lastday
    #dxh:返回前N天
    def getday(self,date,num):
        return str(date+datetime.timedelta(num))
    #dxh:返回上周第一天
    def get_week(self,date):
        thisweekday=datetime.timedelta(days=date.isoweekday())
        sixdays=datetime.timedelta(days=6)
        lastSun=str(date-thisweekday)
        lastMon=str(date-thisweekday-sixdays)
        return lastMon,lastSun

        
        
        







