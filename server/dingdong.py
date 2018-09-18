# -*- coding: utf-8 -*-
'''
    程序入口
'''

import logging
import DingDongConstant
from DingDongRequestHandler import DingDongRequestHandler
from socketserver import ThreadingTCPServer

if __name__ == '__main__':
    #日志配置
    logging.basicConfig(level=logging.DEBUG, \
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', \
                datefmt='%a, %d %b %Y %H:%M:%S', \
                filename=DingDongConstant.LOG_PATH, \
                filemode='a')

    ADDR = (DingDongConstant.SERVER_HOST, DingDongConstant.SERVER_PORT)
    ThreadingTCPServer(ADDR, DingDongRequestHandler).serve_forever()
