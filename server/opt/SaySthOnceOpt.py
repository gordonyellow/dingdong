#_*_ encoding:utf-8 _*_

'''
    播放一次文字内容
'''

import os
import logging
import DingDongConstant

class SaySthOnceOpt:
    '''
        播放一次文字内容
    '''

    def __init__(self, params):
        self.content = params or ''
        logging.info('content=%s', self.content)

    def do(self):
        if self.content:
            os.system("%s %s" % (DingDongConstant.BIN_SAY, self.content))
