#_*_ encoding:utf-8 _*_

'''
    无限次播放文字内容
'''

import os
import DingDongConstant
from DingDongRequestHandler import DingDongRequestHandler
import threading

class SaySthOpt(threading.Thread):
    '''
        无限次播放文字内容
    '''

    def __init__(self, params):
        threading.Thread.__init__(self)
        self.content = params or ''
        DingDongRequestHandler.saySthThreads.append(self)

    def do(self):
        self.start()

    def run(self):
        while True:
            if self.content:
                os.system("%s %s" % (DingDongConstant.BIN_SAY, self.content))
            else:
                DingDongRequestHandler.saySthThreads.remove(self)
                break
