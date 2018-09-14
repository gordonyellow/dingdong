# -*- coding: utf-8 -*-

'''
    服务端
'''

import logging
from time import ctime
import DingDongConstant
from socketserver import StreamRequestHandler

class DingDongRequestHandler(StreamRequestHandler):
    '''
        逻辑处理类
    '''

    saySthThreads = [] #存放播放文字语音的线程
    voiceThreads = [] #存放播放微信语音消息的线程

    def handle(self):
        '''
            具体业务逻辑处理
        '''

        ####################
        #解码
        ####################
        datas = self.rfile.readline()
        if datas:
            datas = datas.strip().decode('UTF-8')
        logging.info('datas=%s', datas)

        ####################
        #根据指令进行相关处理
        ####################
        opt = datas.split(DingDongConstant.SPLIT_FLAG)[0]
        logging.info('opt=%s', opt)
        try:
            optModel = __import__('threads.%s' % opt, fromlist=('%s' % opt))
            optClass = getattr(optModel, opt)
            logging.info('optClass=%s', optClass)
            self.wfile.write(('[%s] %s done' % (ctime(), opt)).encode('UTF-8'))

            optClass(datas).start()
        except ImportError:
            logging.info('optClass=unknow')
            self.wfile.write(('[%s] %s' % (ctime(), datas)).encode('UTF-8'))


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
