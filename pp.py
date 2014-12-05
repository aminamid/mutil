#!/bin/env python
## -*- coding: utf-8 -*-

class color:
    BLUE = '\033[1;34m'
    BLUEL = '\033[0;34m'
    GREEN = '\033[1;32m'
    GREENL = '\033[0;32m'
    CYAN = '\033[1;36m'
    CYANL = '\033[0;36m'
    RED = '\033[1;31m'
    REDL = '\033[0;31m'
    PURPLE = '\033[1;35m'
    PURPLEL = '\033[0;35m'
    YELLOW = '\033[1;33m'
    BROWN = '\033[0;33m'
    WHITE = '\033[1;37m'
    GRAYL = '\033[0;37m'
    GRAYD = '\033[1;30m'
    BLACK = '\033[0;30m'
    ENDC = '\033[0m'

def pretty_convert(obj):
    if isinstance(obj, (float)):
        return u'{1}{2}{0}'.format(color.ENDC, color.PURPLEL, obj)
    elif isinstance(obj, ( bool )):
        return u'{1}{2}{0}'.format(color.ENDC, color.CYAN, obj)
    elif isinstance(obj, ( int, long, complex )):
        return u'{1}{2}{0}'.format(color.ENDC, color.BLUE, obj)
    elif isinstance(obj, ( basestring )):
        return u'{1}"{0}{2}{3}{0}{1}"{0}'.format(color.ENDC, color.REDL, color.RED, obj)
    elif isinstance(obj, ( dict )):
        return dict((u'{1}{2}:{0}'.format(color.ENDC, color.YELLOW,k), pretty_convert(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return map(pretty_convert, obj)
    return obj

def walk_obj(buf, obj, indent_num=2, depth=0, eol='', wrap_len=60, wrap_total=100, lf='\n', maxdepth=None):
    if not maxdepth and depth > maxdepth:
        return
    indent = ' '*indent_num*depth
    buf.write(u'{0}'.format(eol if not eol else eol+indent) )
    if isinstance(obj, (basestring, int, float, complex)):
        buf.write(u'{0}'.format(obj).replace(lf, '{0}{1} '.format(lf, indent)) )
    elif isinstance(obj, ( dict )):
        eol, eol_org = lf, eol
        buf.write('{ ')
        for key in obj.keys():
            buf.write(u'{0}{1}{2}{3} '.format(eol, indent, ' '*indent_num, key))
            walk_obj(buf=buf, obj=obj[key], indent_num=indent_num, depth=depth+1, eol='', wrap_len=wrap_len, lf=lf )
            buf.write(',')
        buf.write('{0}}}'.format(eol if not eol else eol+indent) )
        eol=eol_org
    elif isinstance(obj, (list, tuple)):
        eol_org, indent_org = eol, indent
        for item in obj:
            if isinstance(item, (list, dict)):
                eol = lf
                break
            else:
                eol = ''
                indent = ''
                continue
        if max(map(len,obj)) > wrap_len or sum(map(len,obj)) > wrap_total:
            eol = lf
        buf.write('[ ')
        for item in obj:
            walk_obj(buf=buf, obj=item, indent_num=indent_num, depth=depth+1, eol=eol, wrap_len=wrap_len, lf=lf )
            buf.write(', ')
        buf.write('{0}]'.format(eol if not eol else eol+indent_org) )
        eol, indent = eol_org, indent_org
    if depth == 0:
        buf.write(lf)

def pretty_print(obj, indent=2, b=None):
    if not b:
        import sys, codecs
        b = codecs.getwriter('utf_8')(sys.stdout)
    walk_obj(b, pretty_convert(obj), indent_num=indent)


if __name__ == '__main__':
  import sys
  import codecs
  import json

  if len(sys.argv) < 2:
     raw_data = codecs.getreader('utf_8')(sys.stdin).read()
  else:
     raw_data = codecs.open(sys.argv[1], 'r', 'utf_8').read()

  indent = 2 if len(sys.argv) <3 else int(sys.argv[2])

  parsed_data = None
  try:
      parsed_data = json.loads(raw_data)
  except ValueError as e1:
      #print e1
      try:
          import yaml
          parsed_data = yaml.load(raw_data)
      except yaml.scanner.ScannerError as e2:
          #print e2
          pass
  if not parsed_data:
      sys.exit(2)

  pretty_print(parsed_data, indent)
