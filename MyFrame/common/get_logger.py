#!/usr/bin/env python
# coding=utf-8
# 作者: fujian
# 当前编辑器名: PyCharm

import logging,time
from MyFrame.common.common import Project

class MyLogger:

    logger=None

    @classmethod
    def get_logger(cls):
        if cls.logger==None:
            t=time.strftime('%Y%m%d%H%M%S')
            fh=logging.FileHandler(f'{Project.log_path}/log_{t}.log',mode='w',encoding='utf8')
            sh=logging.StreamHandler()
            fm=logging.Formatter('[%(asctime)s] %(filename)s %(levelname)s: line[%(levelno)s] %(message)s','%Y/%m/%d/%X')
            fh.setFormatter(fm)
            sh.setFormatter(fm)
            cls.logger=logging.getLogger()
            cls.logger.setLevel(logging.INFO)
            cls.logger.addHandler(fh)
            cls.logger.addHandler(sh)
        return cls.logger

