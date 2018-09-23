#_*_ encoding:utf-8 _*_

'''
    停止播放文字内容
'''

from DingDongRequestHandler import DingDongRequestHandler

class StopSaySthOpt:
    '''
        停止播放文字内容
    '''
    def __init__(self, params):
        pass

    def do(self):
        for t in DingDongRequestHandler.saySthThreads:
            t.content = ''
