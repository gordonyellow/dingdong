# -*- coding: utf-8 -*-
'''
测试用客户端
'''

import os
import sys
import socket
import time
import hashlib
from DingDongClient import DingDongClient

HOST = '127.0.0.1'
PORT = 1234
SECRET_KEY = 'yyyw_dingdong_abc123@@'
SPLIT_FLAG = '____@@@____'
BUFFER_SIZE = 1024

class DingDongClient_PlayVoice:
    '''
        测试用客户端类
    '''

    @classmethod
    def doSendDatas(cls, datas, filepath):
        '''
            发送datas到服务端
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(("%s\r\n" % datas).encode())

        with open(filepath, 'rb') as f:
            data = f.read()
            s.sendall(data)

        datas = s.recv(4096)
        print("received from server: %s" % datas.decode())

        s.close()

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/1522202291.837328.amr'
    opt = 'PlayVoice'
    params = 'size=%s&type=amr' % os.path.getsize(filepath)
    print('client send: opt=%s & params=%s' % (opt, params))
    datas = DingDongClient.genDatas(opt, params)
    DingDongClient_PlayVoice.doSendDatas(datas, filepath)
