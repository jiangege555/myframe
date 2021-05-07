#!/usr/bin/env python
# coding=utf-8
# 作者: fujian
# 当前编辑器名: PyCharm

import zipfile
import yagmail
from MyFrame.common.config import *
from MyFrame.common.common import *
from MyFrame.common.get_logger import MyLogger

class Report:

    def __init__(self,version):
        self.version=version
        self.logger=MyLogger.get_logger()

    def write_report(self,module,test_type,case_title,test_result,error,screenshot):
        db=Con_DB(DB_USER,DB_PWD,DB,DB_HOST,DB_PORT)
        now=time.strftime('%Y-%m-%d %H:%M:%S')
        error=error.replace('"','\\"')
        sql=f'''
            insert into report (version,module,type,case_title,result,time,error,screenshot) values
            ("{self.version}","{module}","{test_type}","{case_title}","{test_result}","{now}","{error}","{screenshot}")          
        '''
        db.dml(sql)
        db.close()

    # 生成自定义的html报告
    def generate_report(self):
        db = Con_DB(DB_USER, DB_PWD, DB, DB_HOST, DB_PORT)
        # 检查结果集是否为空
        sql=f'select * from report where version="{self.version}";'
        re=db.query_all(sql)
        if len(re)==0:
            self.logger.error('没找到指定版本的测试结果')
            return None
        # 用例通过数
        sql = f'select count(*) from report where version="{self.version}" and result="成功";'
        success = db.query_one(sql)[0]
        # 用例失败数
        sql = f'select count(*) from report where version="{self.version}" and result="失败";'
        fail = db.query_one(sql)[0]
        # 用例异常数
        sql = f'select count(*) from report where version="{self.version}" and result="异常";'
        error = db.query_one(sql)[0]
        # 结果详情
        sql = f'select * from report where version="{self.version}";'
        res = db.query_all(sql)
        # 最后时间
        sql=f'select time from report where version="{self.version}" order by time desc;'
        last_time=db.query_one(sql)[0]
        # 模板位置
        demo_path=Project.common_path+'/'+'report_demo.html'
        # print(demo_path)
        with open(demo_path,'r',encoding='utf8') as f:
            content=f.read()
            content = content.replace('$version', self.version)
            content = content.replace('$success', str(success))
            content = content.replace('$fails', str(fail))
            content = content.replace('$errors', str(error))
            content = content.replace('$times', str(last_time))
            results = ''
            for i in res:
                if i[5]=='成功':
                    color='lightgreen'
                elif i[5]=='失败':
                    color='yellow'
                else:
                    color='red'
                results += f'''
                                <tr align="center">
				                <td width="3%">{i[0]}</td>
                                <td width="10%">{i[2]}</td>
                                <td width="5%">{i[3]}</td>
                                <td width="15%">{i[4]}</td>
                                <td width="15%">{i[6]}</td>
                                <td width="6%" bgcolor={color}>{i[5]}</td>
                                <td width="16%">{i[7]}</td>\n
                                '''
                if i[8] == '无':
                    results += f'''<td>{i[8]}</td>\n'''
                else:
                    results += f'''<td><a href="{i[8]}">查看截图</a></td>\n'''
            content = content.replace('$results', results)
        with open(Project.report_path + f'/{self.version}_{int(time.time())}.html', 'w', encoding='utf8') as f:
            f.write(content)

    # 压缩测试报告，返回压缩包路径
    def compress_report(self):
        filename=f'report_{self.version}.zip'
        zip_path=os.path.join(Project.report_path,filename)
        zip=zipfile.ZipFile(zip_path,'w',zipfile.ZIP_LZMA)
        filelist=[]
        for root,fdir,fs in os.walk(Project.report_path):
            for file in fs:
                # 过滤掉之前压缩好的zip文件
                if not file.endswith('.zip') and self.version in file:
                    filelist.append(os.path.join(root,file))
            for fd in fdir:
                filelist.append(os.path.join(root,fd))
        for f in filelist:
            zip.write(f,f.split('report',1)[1])
        zip.close()
        return zip_path

    # 将报告以邮件方式发送
    def send_email(self,user,password,attachment,to,host='smtp.163.com'):
        '''
        :param user: 发件人账号
        :param password: 邮箱授权码
        :param attachment: 附件
        :param to:收件人
        :param host: 邮箱服务器，默认163
        :return:
        '''
        # 建立连接
        smtp=yagmail.SMTP(user=user,password=password,host=host)
        # 邮件标题
        subject=f'测试版本为:{self.version}'
        # 邮件正文
        content='详情见附件'
        # with open('../')
        try:
            smtp.send(to=to,subject=subject,contents=content,attachments=attachment)
            self.logger.info(f'邮件发送成功')
        except Exception as e:
            self.logger.error(f'邮件发送失败,原因是 {str(e)}')

if __name__ == '__main__':
    Report('v1.0').compress_report()
