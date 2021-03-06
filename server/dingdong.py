# -*- coding: utf-8 -*-
'''
    程序入口
'''

import os
import logging
from socketserver import ThreadingTCPServer
from DingDongRequestHandler import DingDongRequestHandler
import DingDongConstant

if __name__ == '__main__':
    #日志配置
    logging.basicConfig(level=logging.DEBUG, \
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', \
                datefmt='%a, %d %b %Y %H:%M:%S', \
                filename=DingDongConstant.LOG_PATH, \
                filemode='a')

    with open(DingDongConstant.DING_DONG_PID_FILE, 'wb+') as f:
        f.write(('%s' % os.getpid()).encode())

    ADDR = (DingDongConstant.SERVER_HOST, DingDongConstant.SERVER_PORT)
    ThreadingTCPServer(ADDR, DingDongRequestHandler).serve_forever()
