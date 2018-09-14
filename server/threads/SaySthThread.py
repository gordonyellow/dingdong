#_*_ encoding:utf-8 _*_

'''
    无限次播放文字内容相关处理
'''

import os
import threading
import DingDongConstant
from DingDongRequestHandler import DingDongRequestHandler

class SaySthThread(threading.Thread):
    '''
        用于无限次播放文字内容的线程类
    '''

    def __init__(self, params):
        threading.Thread.__init__(self)
        self.content = params or ''
        DingDongRequestHandler.saySthThreads.append(self)

    def run(self):
        while True:
            if self.content:
                os.system("%s %s" % (DingDongConstant.BIN_SAY, self.content))
            else:
                DingDongRequestHandler.saySthThreads.remove(self)
                break
