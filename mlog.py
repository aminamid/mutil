# coding: utf-8

from os import path,makedirs

from logging import Formatter
from datetime import datetime as dt

def prefix(filepath):
    return path.splitext(path.basename(filepath))[0]

def get_stream_handler(level=10):
    from logging import StreamHandler,Formatter

    handler = StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(Formatter("%(asctime)s %(process)d %(thread)x %(levelname).4s;%(module)s(%(lineno)d/%(funcName)s) %(message)s"))

    return handler

def get_file_handler(filename,level=10):
    from logging import FileHandler,Formatter

    handler = FileHandler(filename=filename)
    handler.setLevel(level)
    handler.setFormatter(Formatter("%(asctime)s %(process)d %(thread)x %(levelname).4s;%(module)s(%(lineno)d/%(funcName)s) %(message)s"))

    return handler

def put_logger(name,handlers=[],level=10):
    from logging import getLogger
    logger = getLogger(name)
    logger.setLevel(level)
    for handler in handlers:
      logger.addHandler(handler)
    return logger

def put_logdir(logprefix, logdir='./log', logpostfixes=[]):
    from datetime import datetime

    date_str = datetime.today().strftime("%Y%m%d%H%M%S")

    if not path.isdir(logdir):  makedirs(logdir)

    logfilenames = []
    for logpostfix in logpostfixes:
      logfilenames.append('{0}/{1}.{2}.{3}'.format(logdir,logprefix,date_str,logpostfix))

    return logfilenames

def convert_ctrl(s):
    return ''.join([chr(x) if x > 31 else '0x{0:0>2x}'.format(x) for x in map(ord,list(s)) ])


from logging import INFO
class HandleManager(object):
    def __init__(self,names, prefix, enable_stream=True, enable_file=True, postfix='log', level=INFO, logdir='./log' ):
        self.file_param = {}
        self.handlers = []
        self.level=level
        if enable_stream:
            self.handlers.append(get_stream_handler())
        if enable_file:
            (log_filename,) = put_logdir(logprefix=prefix, logpostfixes=[postfix])
            self.file_param['logdir']=logdir
            self.file_param['prefix']=prefix
            self.file_param['postfix']=postfix
            self.file_param['basename']=path.splitext(path.basename(log_filename))[0]
            self.handlers.append(get_file_handler(log_filename))
        for name in names:
            put_logger(name=name, level=self.level, handlers=self.handlers)

    def put(self,name):
        put_logger(name=name, level=self.level, handlers=self.handlers)

    def get_file_param(self):
        return self.file_param
if __name__ == '__main__':

    logger  = quicklogger(name=__name__,  enable_stream=True, enable_file=True )

    logger.info('ok')
