#_*_ encoding:utf-8 _*_

'''
    播放音乐相关处理
'''

import os
import threading
import DingDongConstant

class StopPlayMusicThread(threading.Thread):
    '''
        用于播放音乐的线程
    '''

    def __init__(self, params):
        threading.Thread.__init__(self)

    def run(self):
        os.system( \
            'ps -ef|grep "%s"|grep "%s"|awk \'{print $2}\'|xargs kill' % \
            (DingDongConstant.MUSIC_PLAYER, DingDongConstant.DEFAULT_MUSIC) \
        )
