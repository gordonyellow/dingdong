#_*_ encoding:utf-8 _*_

import os
import time
import logging
import threading
import requests
from util.ParamUtil import ParamUtil

BASE_URL = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"

class PlayWeixinVoiceMsgOpt(threading.Thread):
    def __init__(self, paramsStr):
        threading.Thread.__init__(self)
        try:
            params = ParamUtil.getParams(paramsStr)
            self.mediaid = params.get('mediaid') or ''
            self.accesstoken = params.get('accesstoken') or ''
        except Exception as e:
            logging.exception(e)

    def do(self):
        self.start()

    def run(self):
        try:
            filepath = "/var/tmp/%s.amr" % time.time()
            with open(filepath, "wb+") as f:
                r = requests.get(BASE_URL % (self.accesstoken, self.mediaid))
                f.write(r.content)

            for i in range(3):
                os.system("/usr/bin/afplay %s" % filepath)
        except Exception as e:
            logging.exception(e)
