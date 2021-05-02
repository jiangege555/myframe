#!/usr/bin/env python
# coding=utf-8
# 作者: fujian
# 当前编辑器名: PyCharm

import os
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from PIL import ImageGrab
from MyFrame.common.common import Project
from MyFrame.common.get_logger import MyLogger


class UiAction:

    def __init__(self,dr,base_url):
        self.dr=dr
        self.base_url=base_url
        self.logger=MyLogger.get_logger()

    def open_browser(self,url):
        self.dr.get(self.base_url+url)
        self.logger.info(f'打开网址 {self.base_url+url}')

    def get_element(self,locator):
        try:
           ele=self.dr.find_element(*self.get_locator(locator))
           self.logger.info(f'通过 {locator} 定位元素成功')
           return ele
        except Exception as e:
            self.logger.info(f'通过 {locator} 定位元素失败,异常为 {str(e)}')

    def get_locator(self,locator):
        '''
        :param locator: id=username
        :return: id,username
        '''
        by,value=locator.split('=',1)
        by=by.lower()
        # by是id，name，xpath等中的一种
        if by in (By.ID,By.NAME,By.XPATH,By.CLASS_NAME,By.TAG_NAME,By.LINK_TEXT,By.PARTIAL_LINK_TEXT,By.CSS_SELECTOR):
            return by,value
        # by可以不写全，如class，tag
        if By.TAG_NAME.startswith(by):
            return By.TAG_NAME,value
        if By.CLASS_NAME.startswith(by):
            return By.CLASS_NAME,value
        if By.LINK_TEXT.startswith(by):
            return By.LINK_TEXT,value
        if By.PARTIAL_LINK_TEXT.startswith(by):
            return By.PARTIAL_LINK_TEXT,value
        if By.CSS_SELECTOR.startswith(by):
            return By.CSS_SELECTOR,value
        # 如果没写对，默认by id方式
        return By.ID,value

    def input_text(self,locator,text):
        try:
            ele=self.get_element(locator)
            ele.clear()
            ele.send_keys(text)
            self.logger.info(f'在 {locator} 处输入了 {text}')
        except Exception as e:
            self.logger.info(f'在 {locator} 输入 {text} 出现异常,异常为 {str(e)}')

    def click_element(self,locator):
        try:
            self.get_element(locator).click()
            self.logger.info(f'在 {locator} 处做了点击操作')
        except Exception as e:
            self.logger.info(f'点击元素 {locator} 出现异常,异常为 {str(e)}')

    # 等待元素加载完成
    def wait_until(self,locator,timeout=5):
        try:
            return WebDriverWait(self.dr,timeout).until(lambda dr:self.dr.find_element(*self.get_locator(locator)))
        except TimeoutError:
            return None

    # 强制等待
    def sleep(self,timeout):
        time.sleep(int(timeout))

    # # 判断元素是否可见
    # def element_is_visible(self,locator):
    #     return self.wait_until(locator) is not None  # True或False

    # 判断元素是否存在
    def element_is_present(self,locator):
        try:
            self.get_element(locator)
            return True
        except NoSuchElementException:
            return False

    # 断言元素文本包含值
    def element_should_contain(self,locator,except_text):
        assert self.element_is_present(locator),f'指定的元素{locator}没有找到'
        actual=self.get_element(locator).text
        assert except_text in actual,f'实际测试结果{actual}中没有包含期望结果{except_text}'

    # 断言元素文本等于值
    def element_should_be(self,locator,except_text):
        assert self.element_is_present(locator), f'指定的元素{locator}没有找到'
        actual = self.get_element(locator).text
        assert except_text == actual, f'实际测试结果{actual}不等于期望结果{except_text}'

    # 页面源码包含
    def pagesource(self,except_text):
        assert except_text in self.dr.page_source,f'期望结果{except_text}不在页面源码中'

    # 截图
    def screen_shot(self,filename):
        screen_path=os.path.join(Project.report_path,'screenshot')
        img=screen_path+'/'+filename
        ImageGrab.grab().save(img)
        # 返回截图相对路径
        return f'screenshot/{filename}'

    # 刷新页面
    def refresh_page(self):
        self.dr.refresh()

    # 进入框架
    def inframe(self,locator):
        ele=self.get_element(locator)
        self.dr.switch_to.frame(ele)

    # 退出框架
    def paframe(self):
        self.dr.switch_to.parent_frame()

    # 退出最外层框架
    def deframe(self):
        self.dr.switch_to.default_content()

    # 执行js
    def exe_js(self,js,ele=None):
        self.dr.execute_script(js,ele)

