'''
    参数相关
'''

import logging

class ParamUtil:
    '''
        参数相关
    '''

    @classmethod
    def getParams(cls, paramsSrc):
        '''
            获取参数
        '''
        logging.info('ParamUtil.getParams')
        paramDict = dict()
        try:
            for param in paramsSrc.split('&'):
                keyAndValue = param.split('=')
                if keyAndValue and keyAndValue[0]:
                    paramDict[keyAndValue[0]] = keyAndValue[1]
        except:
            logging.exception('参数有误,paramsSrc=%s', paramsSrc)
        return paramDict

    @classmethod
    def getParamKeys(cls, paramsSrc):
        '''
            获取所有参数key
        '''
        keys = []
        for param in paramsSrc.split('&'):
            key = param.split('=')[0]
            if key:
                keys.append(key)
        return keys
