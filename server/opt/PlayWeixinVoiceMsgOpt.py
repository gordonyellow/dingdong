#_*_ encoding:utf-8 _*_

import time
import logging
import requests
from DingDongRequestHandler import DingDongRequestHandler
from opt.PlayVoiceOpt import PlayVoiceProcess
from opt.StopPlayVoiceOpt import StopPlayVoiceOpt
from util.ParamUtil import ParamUtil


BASE_URL = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"

class PlayWeixinVoiceMsgOpt:
    def __init__(self, paramsStr):
        try:
            params = ParamUtil.getParams(paramsStr)
            self.mediaid = params.get('mediaid') or ''
            self.accesstoken = params.get('accesstoken') or ''
        except Exception as e:
            logging.exception(e)

    def do(self):
        logging.info('PlayWeixinVoiceMsgOpt.do')

        #若其他声音文件还在播放中，直接返回
        if not DingDongRequestHandler.playVoiceProcesses.empty():
            logging.info('len=%s', len(DingDongRequestHandler.playVoiceProcesses))
            return "voice playing"

        #生成子进程并放入进程列表中，防止在读取文件时有其他请求进来
        filepath = "/var/tmp/%s.amr" % time.time()
        playVoiceProcess = PlayVoiceProcess(filepath)
        DingDongRequestHandler.playVoiceProcesses.put(filepath)

        try:
            with open(filepath, "wb+") as f:
                r = requests.get(BASE_URL % (self.accesstoken, self.mediaid))
                f.write(r.content)

            playVoiceProcess.start()
        except Exception as e:
            logging.exception(e)
            StopPlayVoiceOpt('').do()
