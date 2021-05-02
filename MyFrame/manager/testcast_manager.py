#!/usr/bin/env python
# coding=utf-8
# 作者: fujian
# 当前编辑器名: PyCharm

from MyFrame.common.common import *
from MyFrame.action.ui_action import UiAction
from MyFrame.action.api_action import ApiAction
import glob,os,traceback,time
from MyFrame.common.config import *
from MyFrame.common.report import Report
from MyFrame.reader.readcsv import ReadCsv


class TestcaseManager:

    def __init__(self,version):
        self.version=version
        self.report=Report(self.version)

    def discovery(self,rule):
        '''
        根据rule找出testcase里的测试脚本
        :param rule: test_ui*,test_api*
        :return:脚本列表
        '''
        testcase=Project.case_path
        return glob.glob(os.path.join(testcase,rule))

    def run(self,path):
        '''
        根据上面找出的脚本，循环调用run方法
        :param path:
        :return:
        '''
        filename=os.path.basename(path)
        test_type='UI测试' if 'ui' in filename else 'API测试'
        if test_type=='UI测试':
            with MyDriver() as driver:
                action =UiAction(driver,BASE_URL)
                self.test(action,test_type,path)
        else:
            with MySession() as session:
                action=ApiAction(session,BASE_URL)
                self.test(action,test_type,path)

    def test(self, action, test_type, path):
        re=ReadCsv(path)
        # print(re.test_module,re.test_title)
        response=None
        try:
            for script in re.scripts:
                method_name = script.pop(0).lower().replace(' ', '_')
                if hasattr(action, method_name):
                    if test_type=='UI测试':
                        getattr(action, method_name)(*script)
                    else:
                        # 含有should的为断言方法，通过code，text，json断言
                        if 'should' in method_name:
                            res=action.get_actual(script,response)
                            getattr(action, method_name)(res,script[0])
                        else:
                            # 处理接口参数
                            if len(script)==1:
                                response=getattr(action, method_name)(*script)
                            else:
                                scr=[script[0],re.dict_data(script[1])]
                                response = getattr(action, method_name)(*scr)
            self.report.write_report(re.test_module,test_type,re.test_title,'成功','无','无')
            action.logger.info(f'模块 {re.test_module} 的用例 {re.test_title} 测试通过')
        except AssertionError as e:
            shot=self.capture_screen(test_type,action)
            # print(str(e))
            self.report.write_report(re.test_module,test_type,re.test_title,'失败',str(e),shot)
            action.logger.error(f'模块 {re.test_module} 的用例 {re.test_title} 测试失败,错误为 {str(e)}')
        except Exception as e:
            shot=self.capture_screen(test_type,action)
            self.report.write_report(re.test_module,test_type,re.test_title,'异常',str(e),shot)
            action.logger.error(f'模块 {re.test_module} 的用例 {re.test_title} 测试出异常,异常为 {traceback.format_exc()}')

    def capture_screen(self,test_type,action):
        if test_type=='UI测试':
            filename=f'{self.version}_{time.strftime("%Y%m%d%H%M%S")}.jpg'
            return action.screen_shot(filename)
        return '无'

    def build_report(self):
        self.report.generate_report()

    def send_report(self):
        path=self.report.compress_report()
        self.report.send_email(EMAIL_SENDER,EMAIL_PWD,path,EMAIL_REC,EMAIL_HOST)

if __name__ == '__main__':
    tm=TestcaseManager('v1.1')
    case=tm.discovery('*')
    # print(case)
    for i in case:
        print(i)
        tm.run(i)
    tm.build_report()
    tm.send_report()