# -*- coding: utf-8 -*-

BASE_CONFIG = """---
version: 1 
disable_existing_loggers: False
loggers:
  foo.bar.baz:
    handlers: [console, file]
handlers:
  console:
    class : logging.StreamHandler
    formatter: mx
    level: {level}
    stream: ext://sys.stdout
  file:
    class : logging.handlers.TimedRotatingFileHandler
    formatter: mx
    level: {level}
    filename: {dir}/{filename}
    when: 'H'
    interval: 24
    backupCount: 365
formatters:
  mx:
    format: '%(asctime)s %(process)d %(thread)x %(levelname).4s;%(module)s(%(lineno)d/%(funcName)s) %(message)s'
    datefmt: '%Y%m%d %H%M%S'
"""

from logging import INFO

def gencfg(
        names,
        prefix,
        enable_stream=True,
        enable_file=True,
        postfix='log',
        level=INFO,
        logdir='./log',
           ):
    global yaml
    import yaml
    global os
    import os

    dirpath=os.path.abspath(logdir)
    if enable_file and not os.path.isdir(dirpath):  os.makedirs(dirpath)

    tmp_handlers = []
    if enable_stream:  tmp_handlers.append('console')
    if enable_file:    tmp_handlers.append('file')

    loggers_dict = dict([ ( x, {'handlers': tmp_handlers } ) for x in names ])
    
    cfg_dict = yaml.load( 
        BASE_CONFIG.format( **{ 'level': level, 'dir': dirpath, 'filename': '{0}.{1}'.format(prefix, postfix) } )
    )
    cfg_dict.update(loggers_dict)
    return cfg_dict

def prefix(filepath):
    global os
    import os
    return os.path.splitext(os.path.basename(filepath))[0]

def convert_ctrl(s):
    return ''.join([chr(x) if x > 31 else '0x{0:0>2x}'.format(x) for x in map(ord,list(s)) ])


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
