#_*_ encoding:utf-8 _*_

'''
    播放音乐相关处理
'''

import os
import threading
import DingDongConstant

class PlayMusicThread(threading.Thread):
    '''
        用于播放音乐的线程
    '''

    def __init__(self, params):
        threading.Thread.__init__(self)

    def run(self):
        os.system('%s %s &' % (DingDongConstant.MUSIC_PLAYER, DingDongConstant.DEFAULT_MUSIC))
