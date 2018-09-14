#_*_ encoding:utf-8 _*_

'''
    停止播放文字内容
'''

import threading
from DingDongRequestHandler import DingDongRequestHandler

class StopSayThread(threading.Thread):
    '''
        用于停止播放文字内容的线程类
    '''
    def __init__(self, datas):
        threading.Thread.__init__(self)

    def run(self):
        for t in DingDongRequestHandler.saySthThreads:
            t.content = ''
