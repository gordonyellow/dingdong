#_*_ encoding:utf-8 _*_

'''
    打印相关消息
'''

import threading
import logging
import DingDongConstant
from DingDongRequestHandler import DingDongRequestHandler

class PrintInfoThread(threading.Thread):
    '''
        用于打印相关消息的线程
    '''
    def __init__(self, datas):
        threading.Thread.__init__(self)
        datas_array = datas.split(DingDongConstant.SPLIT_FLAG)
        self.goal = datas_array[1] if len(datas_array) >= 1 else ''

    def run(self):
        if self.goal == 'DingDongRequestHandler.saySthThreads':
            logging.info('DingDongRequestHandler.saySthThreads=%s', DingDongRequestHandler.saySthThreads)
