#_*_ encoding:utf-8 _*_
import os

class LockMacMiniOpt:
    def __init__(self, params):
        pass

    def do(self):
        os.system("/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend &")
