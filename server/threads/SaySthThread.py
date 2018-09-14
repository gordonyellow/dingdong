#_*_ encoding:utf-8 _*_

'''
    无限次播放文字内容相关处理
'''

import os
import threading
import logging
import DingDongConstant
from DingDongRequestHandler import DingDongRequestHandler

class SaySthThread(threading.Thread):
    '''
        用于无限次播放文字内容的线程类
    '''

    def __init__(self, datas):
        threading.Thread.__init__(self)
        datas_array = datas.split(DingDongConstant.SPLIT_FLAG)
        self.content = datas_array[1] if len(datas_array) >= 1 else ''
        DingDongRequestHandler.saySthThreads.append(self)

    def run(self):
        while True:
            if self.content:
                os.system("%s %s" % (DingDongConstant.BIN_SAY, self.content))
            else:
                DingDongRequestHandler.saySthThreads.remove(self)
                break
