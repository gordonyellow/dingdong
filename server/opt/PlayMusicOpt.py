#_*_ encoding:utf-8 _*_

'''
    播放音乐相关处理
'''

import os
import DingDongConstant

class PlayMusicOpt:
    '''
        播放音乐
    '''

    def __init__(self, params):
        pass

    def do(self):
        os.system('%s %s &' % (DingDongConstant.MUSIC_PLAYER, DingDongConstant.DEFAULT_MUSIC))
