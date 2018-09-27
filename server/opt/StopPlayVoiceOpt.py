#_*_ encoding:utf-8 _*_

'''
    停止播放声音文件
'''

import os
import logging
import DingDongConstant
from DingDongRequestHandler import DingDongRequestHandler

class StopPlayVoiceOpt:
    '''
        停止播放声音文件
    '''
    def __init__(self, params):
        pass

    def do(self):
        try:
            while not DingDongRequestHandler.playVoiceProcesses.empty():
                voiceFilePath = DingDongRequestHandler.playVoiceProcesses.get()
                logging.info("voiceFilePath=%s", voiceFilePath)

                #杀父进程
                os.system( \
                    'ps -ef|grep "%s"|grep "%s"|awk \'{print $3}\'|xargs kill &' % \
                    (DingDongConstant.MUSIC_PLAYER, voiceFilePath) \
                )
                logging.info('kill parent process done')

                #杀子进程
                os.system( \
                    'ps -ef|grep "%s"|grep "%s"|awk \'{print $2}\'|xargs kill &' % \
                    (DingDongConstant.MUSIC_PLAYER, voiceFilePath) \
                )
                logging.info('kill child process done')

                #删除声音文件
                os.remove(voiceFilePath)
        except Exception as e:
            logging.exception(e)
