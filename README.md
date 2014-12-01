# Feature

Below is the skelton for parsing and validating commandline arguments, and logging.

```python
# -*- coding: utf-8 -*-

from logging import getLogger

module_logger = getLogger(__name__)

def parsed_args():
    from mutil import mopts
    from mutil.schema import Schema, And, Use, Or, Optional, SchemaError

    myhelp = """
    Usage:
      {progname} [options] [(--logfile | --logboth)] [(--debug | --nolog)] ARGS...

    Options:
      --logfile             out put log to file  [default: False]
      --logboth             out put log to file and console  [default: False]
      --logdir DIR          out put log to file  [default: ./dir]
      --loglevel <level>    loglevel [default: 20]
      --debug               set loglevel to logging.DEBUG [default: False]
      --nolog               set loglevel to 0 [default: False]
      --help                show this message

    """
    myschema = Schema({
      'ARGS': list,

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
    module_logger.info('opts=[{0}]'.format(opts))

    print(opts)


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

    main(opts, handle_mgr)
```


