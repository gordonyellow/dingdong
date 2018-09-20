# -*- coding: utf-8 -*-

'''
    服务端
'''

import hashlib
import logging
import time
from time import ctime
from socketserver import StreamRequestHandler
import DingDongConstant

class DingDongRequestHandler(StreamRequestHandler):
    '''
        逻辑处理类
    '''

    saySthThreads = [] #存放播放文字语音的线程
    voiceThreads = [] #存放播放微信语音消息的线程

    @classmethod
    def getOptClass(cls, datas):
        '''
            从接收的数据中获取实际opt类
            @param datas 字符串 接收的数据
            @return (optClass, opt, optParams) 由opt类,opt及opt参数组成的tuple实例
        '''
        optClass = None
        opt = ''
        optParams = ''
        try:
            opt = datas.split(DingDongConstant.SPLIT_FLAG)[0]
            optParams = datas.split(DingDongConstant.SPLIT_FLAG)[1]
            logging.info('opt=%s', opt)
            logging.info('optParams=%s', optParams)

            optModel = __import__('threads.%s' % opt, fromlist=('%s' % opt))
            optClass = getattr(optModel, opt)
        except ImportError:
            logging.info('import error in getOptClass')
        logging.info('optClass=%s', optClass)
        return (optClass, opt, optParams) if optClass else None

    @classmethod
    def auth(cls, datas):
        '''
            授权校验
            datas组成应该为${opt}${split_flag}${params}${split_flag}${timestamp}${split_flag}${token}
        '''
        datasSplited = datas.split(DingDongConstant.SPLIT_FLAG)

        #数据组成有误
        if len(datasSplited) != 4:
            logging.info('auth failed,datas error')
            return False

        opt = datasSplited[0]
        params = datasSplited[1]
        timestamp = datasSplited[2]
        token = datasSplited[3]

        #时间参数有误
        if not (timestamp and timestamp.isdigit()):
            logging.info('auth failed,timestamp error')
            return False

        #5分钟前的请求忽略
        timeNow = time.time()
        if abs(timeNow - int(timestamp)) > 5*60:
            logging.info('auth failed,timestamp less than 300 seconds')
            return False

        #检验token
        tokenSrc = "%s|%s|%s|%s" % (opt, params, timestamp, DingDongConstant.SECRET_KEY)
        goalToken = hashlib.md5(tokenSrc.encode("utf8")).hexdigest()
        return token == goalToken


    def handle(self):
        '''
            具体业务逻辑处理
        '''

        while True:
            ####################
            #读取客户端数据
            #如果读取时抛出异常，说明客户端已经断开连接，服务端也直接断开
            ####################
            datas = ''
            try:
                datas = self.rfile.readline()
            except:
                logging.info('catch exception in handle')
                break #断开连接

            ####################
            #解码及授权校验
            ####################
            datas = datas.strip().decode('UTF-8')
            logging.info('datas=%s', datas)
            if not DingDongRequestHandler.auth(datas):
                self.wfile.write(('[%s] auth failed' % ctime()).encode('UTF-8'))
                logging.info('auth failed')
                continue

            ####################
            #解析指令并执行
            ####################
            (optClass, opt, optParams) = DingDongRequestHandler.getOptClass(datas)
            response = '[%s] unknow opt' % ctime()
            if optClass is not None:
                optClass(optParams).start()
                response = '[%s] %s called' % (ctime(), opt)
            self.wfile.write(response.encode('UTF-8'))


        '''
        if datas == 'play_music': #播放音乐
            os.system('%s %s &' % (DingDongConstant.MUSIC_PLAYER, DingDongConstant.DEFAULT_MUSIC))
            logging.info('opt=paly_music')
            self.wfile.write(('[%s] %s' % (ctime(), 'play music done')).encode('UTF-8'))
        elif datas == 'stop_play_music': #停止播放音乐
            os.system( \
                'ps -ef|grep "%s"|grep "%s"|awk \'{print $2}\'|xargs kill' % \
                (DingDongConstant.MUSIC_PLAYER, DingDongConstant.DEFAULT_MUSIC) \
            )
            logging.info('opt=stop_play_music')
            self.wfile.write(('[%s] %s' % (ctime(), 'stop play music done')).encode('UTF-8'))
        elif datas.startswith('___say_once___'): #将文字转语音并播放一次
            msgToSayOnce = datas.replace('___say_once___', '')
            saySthOnceThread = SaySthOnceThread(msgToSayOnce)
            saySthOnceThread.start()
            logging.info('opt=___say_once___')
            self.wfile.write(('[%s] %s' % (ctime(), '%s done' % datas)).encode('UTF-8'))
        elif datas.startswith('___say___'): #将文字转语音无限播放
            msgToSay = datas.replace('___say___', '')
            saySthThread = SaySthThread(msgToSay)
            saySthThread.start()
            DingDongRequestHandler.saySthThreads.append(saySthThread)
            logging.info('opt=___say___')
            self.wfile.write(('[%s] %s' % (ctime(), '%s done' % datas)).encode('UTF-8'))
        elif datas == 'stop_say': #停止播放由文字转成的语音
            for t in DingDongRequestHandler.saySthThreads:
                t.content = ''
            logging.info('opt=stop_say')
            self.wfile.write(('[%s] %s' % (ctime(), '%s done' % datas)).encode('UTF-8'))
        elif datas == '___lock___':
            lockThread = LockThread()
            lockThread.start()
            logging.info('opt=___lock___')
            self.wfile.write(('[%s] %s' % (ctime(), '%s done' % datas)).encode('UTF-8'))
        elif datas.startswith('___voice___'): #播放微信语音消息
            voiceThread = VoiceThread(datas)
            voiceThread.start()
            DingDongRequestHandler.voiceThreads.append(voiceThread)
            logging.info('opt=___voice___')
            self.wfile.write(('[%s] %s' % (ctime(), '%s done' % datas)).encode('UTF-8'))
        elif datas.startswith('___stop_voice___'): #停止播放微信语音消息
            for t in DingDongRequestHandler.voiceThreads:
                t.content = ''
            logging.info('opt=stop_voice')
            self.wfile.write(('[%s] %s' % (ctime(), '%s done' % datas)).encode('UTF-8'))
        elif datas == '___open_relay___': #打开继电器
            RelayThread(content=0).start()
        elif datas == '___close_relay___': #关闭继电器
            RelayThread(content=3).start()
        else: #未定义消息原文返回
            logging.info('opt=unknow')
            self.wfile.write(('[%s] %s' % (ctime(), datas)).encode('UTF-8'))
        '''
