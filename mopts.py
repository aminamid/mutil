# -*- coding: utf-8 -*-

def parse(myhelp, myschema, filepath):
    import sys
    from os import path
    from docopt import docopt
    from collections import namedtuple
    from logging import DEBUG
    from schema import SchemaError 

    parsed_opts = docopt( myhelp.format(progname = path.basename(filepath), basename = path.splitext(path.basename(filepath))[0]), version=None )
    
    if parsed_opts['--loglevel']:
        print 'docopt parsed as below:\n{0}'.format(parsed_opts)

    checked_opts = myschema.validate(parsed_opts)

    if checked_opts['--nolog']: checked_opts['--loglevel'] = 0
    if checked_opts['--debug']: checked_opts['--loglevel'] = DEBUG

    opts_keys = [ x for x in checked_opts.keys() ]

    opts = namedtuple('Opts',' '.join( [x.strip('-<>') for x in opts_keys] ))(*tuple([checked_opts[x] for x in opts_keys]))

    return opts

