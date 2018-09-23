#_*_ encoding:utf-8 _*_

import os
import logging

class OpenTeamViewerOpt():
    '''
        打开TeamView
    '''
    def __init__(self, params):
        pass

    def run(self):
        logging.info('OpenTeamViewer')
        try:
            os.system('/usr/bin/open /Applications/TeamViewer.app &')
        except Exception as e:
            logging.exception(e)
