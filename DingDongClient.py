# -*- coding: utf-8 -*-
'''
测试用客户端
'''

import sys
import socket
import time
import hashlib

HOST = '127.0.0.1'
PORT = 1234
SECRET_KEY = 'dingdong_abc123@@'
SPLIT_FLAG = '____@@@____'

class DingDongClient:
    '''
        测试用客户端类
    '''

    @classmethod
    def doSendDatas(cls, datas):
        '''
            发送datas到服务端
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(("%s\r\n" % datas).encode())

        datas = s.recv(4096)
        print(datas.decode())

        s.close()

    @classmethod
    def genDatas(cls, opt, params):
        '''
            根据指令及指令参数生成发送的数据
        '''
        timeNow = time.time() - 60*3
        timestamp = '%s' % int(timeNow)
        tokenSrc = '%s|%s|%s|%s' % (opt, params, timestamp, SECRET_KEY)
        token = hashlib.md5(tokenSrc.encode("utf8")).hexdigest()
        return SPLIT_FLAG.join([opt, params, timestamp, token])

if __name__ == "__main__":
    opt = sys.argv[1] if len(sys.argv) > 1 else 'PlayMusicThread'
    params = sys.argv[2] if len(sys.argv) > 2 else ''
    datas = DingDongClient.genDatas(opt, params)
    DingDongClient.doSendDatas(datas)
    print("done")
