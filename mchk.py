# check code doesn't use reserved word
import sys
import re
import codecs
import operator as op

ngset = set(op.add(__import__('keyword').kwlist, dir(__builtins__)) ) 

code = codecs.getreader('utf_8')(sys.stdin).read()

usedset = set(map( lambda x: x.strip(), re.split('[\"\'\[\]= :\(\),\.<>\{\}\*]', code) ))

for word in sorted(ngset & usedset):
    print word

