#_*_ encoding:utf-8 _*_
'''
    打印相关消息
'''

import logging
from DingDongRequestHandler import DingDongRequestHandler

class PrintInfoOpt:
    '''
        打印相关消息
    '''
    def __init__(self, params):
        self.goal = params

    def do(self):
        if self.goal == 'DingDongRequestHandler.saySthThreads':
            logging.info('DingDongRequestHandler.saySthThreads=%s', DingDongRequestHandler.saySthThreads)
