#!/usr/bin/env python
# coding=utf-8
# 作者: fujian
# 当前编辑器名: PyCharm

import jsonpath
from MyFrame.common.get_logger import MyLogger

class ApiAction:

    def __init__(self,session,base_url):
        self.session=session
        self.base_url=base_url
        self.logger=MyLogger.get_logger()

    def get(self,uri, **kwargs):
        resp=self.session.get(f'{self.base_url}{uri}',**kwargs)
        self.logger.info(f'请求的url地址为 {resp.request.url},请求头为 {resp.request.headers},请求正文为 {resp.request.body}')
        return resp

    def post(self,uri, data=None,json=None,**kwargs):
        resp=self.session.post(f'{self.base_url}{uri}',data,json,**kwargs)
        self.logger.info(f'请求的url地址为 {resp.request.url},请求头为 {resp.request.headers},请求正文为 {resp.request.body}')
        return resp

    def put(self,uri,data=None,**kwargs):
        resp=self.session.post(f'{self.base_url}{uri}', data,**kwargs)
        self.logger.info(f'请求的url地址为 {resp.request.url},请求头为 {resp.request.headers},请求正文为 {resp.request.body}')
        return resp

    def delete(self,uri,**kwargs):
        resp=self.session.post(f'{self.base_url}{uri}',**kwargs)
        self.logger.info(f'请求的url地址为 {resp.request.url},请求头为 {resp.request.headers},请求正文为 {resp.request.body}')
        return resp

    def status_should_be(self,code,ex):
        assert str(code)==ex ,f'请求的响应码{code}与预期结果{ex}不一致'

    def should_be_equal(self,actual,ex):
        assert actual==ex,f'请求的响应内容{actual}与预期结果{ex}不相等'

    def should_be_contain(self,actual,ex):
        assert ex in actual,f'请求的相应内容为{actual}，不包含{ex}'

    def get_actual(self,script,response):
        '''
        提供了三种断言方式，code，text，json
        :param script: 读取脚本的一行数据
        :param response: 发送请求后的对象
        :return: 返回具体的实际响应
        '''
        response_type=script.pop(0)
        if response_type=='code':
            return response.status_code
        if response_type=='text':
            return response.text
        if response_type.startswith('json'):
            json_path=response_type.replace('json','')
            return jsonpath.jsonpath(response.json(),json_path)
        return None
