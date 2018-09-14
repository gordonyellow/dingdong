#_*_ encoding:utf-8 _*_

import os
import time
import logging
import threading
import requests

BASE_URL = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"

class VoiceThread(threading.Thread):
    def __init__(self, content, group=None, target=None, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self.content = content

    def run(self):
        try:
            datas = self.content.split("&")
            mediaid = datas[1]
            accesstoken = datas[2]
            filepath = "/var/tmp/%s.amr" % time.time()
            with open(filepath, "wb+") as f:
                r = requests.get(BASE_URL % (accesstoken, mediaid))
                f.write(r.content)

            while True:
                if self.content:
                    os.system("/usr/bin/afplay %s" % filepath)
                else:
                    break
        except Exception as e:
            logging.exception(e)
