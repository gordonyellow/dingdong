#_*_ encoding:utf-8 _*_

import logging
from DingDongRequestHandler import DingDongRequestHandler

class CheckPlayVoiceOpt:
    '''
        检查是否可以播放声音文件
    '''

    def __init__(self, params):
        pass

    def do(self):
        logging.info("CheckPlayVoiceOpt")
        if not DingDongRequestHandler.playVoiceProcesses.empty():
            return "wait"
        else:
            return "ok"
