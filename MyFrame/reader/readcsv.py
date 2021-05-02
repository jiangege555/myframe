#!/usr/bin/env python
# coding=utf-8
# 作者: fujian
# 当前编辑器名: PyCharm

import os,csv
from MyFrame.common.common import Project

class ReadCsv:

    def __init__(self,path):
        self.count=0
        self._scripts=self.__reader__(path)

    def __reader__(self,path):
        # path = case_path + '/' + filename
        # 排除文件不存在或者是目录的情况
        try:
            if not os.path.exists(path) or os.path.isdir(path):
                return None
            self.count+=1
            with open(path,'r',encoding='utf8') as f:
                reader=csv.reader(f)
                # 只有第一次才取模块名和用例标题
                if self.count==1:
                    self._module,self._title=reader.__next__()
                else:
                    reader.__next__()
                scripts=[]
                # 用例中嵌套另一个用例，比如需要登录后才能进行后续操作
                for i in reader:
                    if i[0].endswith('.txt') or i[0].endswith('.csv'):
                        sub_scripts=self.__reader__(os.path.join(Project.case_path,i[0]))
                        # 如果有嵌套，把嵌套的用例每行添加到一个列表中
                        scripts.extend(sub_scripts)
                    else:
                        scripts.append(i)
                return scripts
        except Exception as e:
            print(e)

    @property
    def scripts(self):
        return self._scripts

    @property
    def test_module(self):
        return self._module

    @property
    def test_title(self):
        return self._title

    @staticmethod
    def dict_data(data):
        dict_data={}
        for i in data.strip().split('&'):
            k,v=i.strip().split('=')
            dict_data[k]=v
        return dict_data

if __name__ == '__main__':
    re=ReadCsv(r'D:\PyCharm\ui\MyFrame\testcase\test_ui_add_customer.txt')
    print(re.scripts)
    # print(re.dict_data('username=admin&password=123456&verifycode=0000'))