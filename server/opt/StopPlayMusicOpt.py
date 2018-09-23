#_*_ encoding:utf-8 _*_

'''
    停止播放音乐
'''

import os
import DingDongConstant

class StopPlayMusicOpt:
    '''
        用于播放音乐的线程
    '''

    def __init__(self, params):
        pass

    def do(self):
        os.system( \
            'ps -ef|grep "%s"|grep "%s"|awk \'{print $2}\'|xargs kill' % \
            (DingDongConstant.MUSIC_PLAYER, DingDongConstant.DEFAULT_MUSIC) \
        )
