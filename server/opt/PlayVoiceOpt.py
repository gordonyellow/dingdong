#_*_ encoding:utf-8 _*_

import os
import time
import logging
from util.ParamUtil import ParamUtil

class PlayVoiceOpt:
    '''
        播放声音文件
    '''

    def __init__(self, paramsStr, rfile):
        params = ParamUtil.getParams(paramsStr)
        self.voiceType = params.get('type') or 'amr'
        self.voiceSize = int(params.get('size') or 0)
        self.rfile = rfile
        self.currentSize = 0
        self.bufferSize = 1024
        self.playFlag = True

    def do(self):
        try:
            filepath = "/var/tmp/%s.%s" % (time.time(), self.voiceType)
            logging.info('filepath=%s', filepath)
            with open(filepath, "wb+") as f:
                while True:
                    goalSize = self.bufferSize
                    goalSize = self.voiceSize - self.currentSize
                    if goalSize > self.bufferSize:
                        goalSize = self.bufferSize
                    if goalSize == 0:
                        break
                    f.write(self.rfile.read(goalSize))
                    self.currentSize += goalSize

            while True:
                if self.playFlag:
                    os.system("/usr/bin/afplay %s" % filepath)
                else:
                    break
        except Exception as e:
            logging.exception(e)
