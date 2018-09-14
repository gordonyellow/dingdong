#_*_ encoding:utf-8 _*_

'''
    播放一次文字内容
'''

import os
import threading
import logging
import DingDongConstant

class SaySthOnceThread(threading.Thread):
    '''
        用于播放一次文字内容的线程类
    '''

    def __init__(self, datas):
        threading.Thread.__init__(self)
        datas_array = datas.split(DingDongConstant.SPLIT_FLAG)
        self.content = datas_array[1] if len(datas_array) >= 1 else ''
        logging.info('content=%s', self.content)

    def run(self):
        if self.content:
            os.system("%s %s" % (DingDongConstant.BIN_SAY, self.content))
