#_*_ encoding:utf-8 _*_
import threading
import os

class LockThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group, target, name, args, kwargs)

    def run(self):
        try:
            os.system("/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend")
        except Exception as e:
            print(e)
