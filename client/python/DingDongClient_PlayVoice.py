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

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/1522202291.837328.amr'
    filetype = filepath.split('.')[-1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    #检查是否有声音文件正在播放
    opt = 'CheckPlayVoice'
    params = ''
    print('client send: opt=%s & params=%s' % (opt, params))
    datas = DingDongClient.genDatas(opt, params)
    s.send(("%s\r\n" % datas).encode())
    response = s.recv(4096).decode()

    print("received from server: %s" % response)
    if response == "wait":
        print('声音文件播放中，请稍后重试')
    elif response == "ok":
        opt = 'PlayVoice'
        params = 'size=%s&type=%s' % (os.path.getsize(filepath), filetype)
        print('client send: opt=%s & params=%s' % (opt, params))
        datas = DingDongClient.genDatas(opt, params)
        s.send(("%s\r\n" % datas).encode())

        with open(filepath, 'rb') as f:
            data = f.read()
            s.sendall(data)

        datas = s.recv(4096)
        print("received from server: %s" % datas.decode())

    s.close()
