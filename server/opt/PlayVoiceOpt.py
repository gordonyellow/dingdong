#_*_ encoding:utf-8 _*_

import os
import time
import logging
from multiprocessing import Process
import DingDongConstant
from DingDongRequestHandler import DingDongRequestHandler
from util.ParamUtil import ParamUtil
from opt.StopPlayVoiceOpt import StopPlayVoiceOpt

class PlayVoiceProcess(Process):
    '''
        播放声音文件子进程
    '''
    def __init__(self, voiceFilePath):
        Process.__init__(self)
        self.voiceFilePath = voiceFilePath

    def run(self):
        logging.info('PlayVoiceProcess.run')
        for i in range(10): #默认播放10次
            logging.info('playing voice %s', i)
            os.system("%s %s" % (DingDongConstant.MUSIC_PLAYER, self.voiceFilePath))
        logging.info('PlayVoiceProcess.run:play voice done')
        StopPlayVoiceOpt('').do()

class PlayVoiceOpt:
    '''
        播放声音文件
    '''

    def __init__(self, paramsStr, rfile):
        params = ParamUtil.getParams(paramsStr)
        self.voiceType = params.get('type') or 'amr' #声音文件类型，如amr,m41,mp3等
        self.voiceSize = int(params.get('size') or 0) #声音文件大小
        self.rfile = rfile #用于从socket中读取文件内容
        self.currentSize = 0 #当前已读取的文件大小
        self.bufferSize = 1024 #文件缓冲区大小

    def do(self):
        logging.info('PlayVoiceOpt.do')

        #若其他声音文件还在播放中，直接返回
        if not DingDongRequestHandler.playVoiceProcesses.empty():
            logging.info('len=%s', len(DingDongRequestHandler.playVoiceProcesses))
            return "voice playing"

        #生成子进程并放入进程列表中，防止在读取文件时有其他请求进来
        filepath = "/var/tmp/%s.%s" % (time.time(), self.voiceType)
        playVoiceProcess = PlayVoiceProcess(filepath)
        DingDongRequestHandler.playVoiceProcesses.put(filepath)

        try:
            with open(filepath, "wb+") as f:
                while True:
                    goalSize = self.voiceSize - self.currentSize
                    if goalSize > self.bufferSize:
                        goalSize = self.bufferSize
                    if goalSize == 0:
                        break
                    f.write(self.rfile.read(goalSize))
                    self.currentSize += goalSize

            playVoiceProcess.start()
        except Exception as e:
            logging.exception(e)
            StopPlayVoiceOpt('').do()
