#!/usr/bin/env python
# coding=utf-8
# 作者: fujian
# 当前编辑器名: PyCharm

import os,pymysql
import time,requests
from selenium import webdriver

class MyDriver:

    def __init__(self,browser_type='chrome'):
        if browser_type.lower()== 'firefox' or browser_type.lower()=='ff':
            self.dr=webdriver.Firefox()
            self.dr.maximize_window()
            time.sleep(3)
        elif browser_type.lower()== 'chrome' or browser_type.lower()=='gc':
            self.dr = webdriver.Chrome()
            self.dr.maximize_window()
            time.sleep(3)
        else:
            print('目前只支持火狐和谷歌')

    def __enter__(self):
        return self.dr

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dr.quit()

class MySession:

    def __init__(self):
        self.session=requests.session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

class Project:

    base_path = os.path.dirname(os.path.dirname(__file__))
    common_path=os.path.dirname(__file__)
    case_path = os.path.join(base_path, 'testcase')
    log_path = os.path.join(base_path, 'log')
    report_path = os.path.join(base_path, 'report')
    page_path = os.path.join(base_path, 'page')

class Con_DB:
    def __init__(self,user,password,db,host='localhost',port=3307,charset='utf8'):
        self.user = user
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.charset = charset
        self.con = None
        self.cur = None
        self.con_db()
    def con_db(self):
        try:
            self.con = pymysql.connect(user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      port=self.port,
                                      db=self.db,
                                      charset=self.charset)
        except Exception as e:
            print(e)
        else:
            self.cur = self.con.cursor()
    def query_all(self,sql):
        """查询返回多行数据"""
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            return str(e)
    def query_one(self,sql):
        """查询返回一行数据"""
        try:
            self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception as e:
            return str(e)
    def dml(self,*sql):
        """DML操作"""
        try:
            for i in sql:
                self.cur.execute(i)
        except Exception as e:
            print(e)
            self.con.rollback()
            return str(e)
        else:
            self.con.commit()
            return True
    def close(self):
        self.cur.close()
        self.con.close()