# Feature


```python
# -*- coding: utf-8 -*-

from logging import getLogger

module_logger = getLogger(__name__)

def parsed_args():
    from mutil import mopts
    from mutil.schema import Schema, And, Use, Or, Optional, SchemaError

    myhelp = """
    Usage:
      {progname} [options] [(--logfile | --logboth)] [(--debug | --nolog)]  get (<query> | -f FILE)
      {progname} [options] [(--logfile | --logboth)] [(--debug | --nolog)]  put (<influxdb_point> | -f FILE)
      {progname} [options] [(--logfile | --logboth)] [(--debug | --nolog)]  getdb
      {progname} [options] [(--logfile | --logboth)] [(--debug | --nolog)]  getcq
      {progname} [options] [(--logfile | --logboth)] [(--debug | --nolog)]  dropcq <cqid>
      {progname} [options] [(--logfile | --logboth)] [(--debug | --nolog)]  dropcq_all

    Options:
      -h HOST, --host=HOST  hostname [default: localhost]
      -p PORT, --port=PORT  port number [default: 8086]
      -u USER, --user=USER  user for influxdb [default: root]
      -w PSWD, --pswd=PSWD  password for influxdb [default: root]
      -d DB, --dbname=DB    dbname [default: testdb]
      -t TIMEOUT, --timeout=TIMEOUT    dbname [default: 60]
      -f FILE, --file=FILE  filename
      --force               force create if db is not exists [default: False]
      --logfile             out put log to file  [default: False]
      --logboth             out put log to file and console  [default: False]
      --logdir DIR          out put log to file  [default: ./dir]
      --loglevel <level>    loglevel [default: 30]
      --debug               set loglevel to logging.DEBUG [default: False]
      --nolog               set loglevel to 0 [default: False]
      --help                show this message

    """
    myschema = Schema({
      'get':bool,
      'put':bool,
      'getdb':bool,
      'getcq':bool,
      'dropcq':bool,
      'dropcq_all':bool,
      '<query>': Or(None, str),
      '<influxdb_point>': Or(None, str),
      '<cqid>': Or(None, Use(int)),
      '--host': basestring,
      '--port': Use(int),
      '--user': basestring,
      '--pswd': basestring,
      '--dbname': basestring,
      '--timeout': Use(int),
      '--file': Or(None, Use(open, error="Files should be readable")),
      '--force': bool,
      '--logfile': bool,
      '--logboth': bool,
      '--logdir': basestring,
      '--loglevel': Or(None, Use(int)),
      '--debug': bool,
      '--nolog': bool,
      '--help': bool,
      })

    return mopts.parse(myhelp=myhelp, myschema=myschema, filepath=__file__)

def main(opts, handle_mgr  ):
    module_logger.info('args=[{0}],opts=[{1}]'.format(args,opts))


if __name__ == '__main__':
    from mutil import mlog
    opts = parsed_args()

    logging_modules=[ __name__ ]

    handle_mgr = mlog.HandleManager(
        names = logging_modules,
        logdir = opts.logdir,
        prefix = mlog.prefix(__file__),
        postfix = 'log',
        enable_stream = not opts.logfile ,
        enable_file = opts.logboth or opts.logfile,
        level = opts.loglevel )
```


