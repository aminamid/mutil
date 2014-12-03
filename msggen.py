# -*- coding: utf-8 -*-

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import mimetypes
import yaml
from random import choice

class BlackBox(object):
    def __init__(self, spec_table):
        self.index = []
        hash = []
        for key in spec_table:
            id=len(self.index)
            self.index.append( key )
            hash.append([id for x in range(spec_table[key]['weight'])])
        self.hash = [ x for inner_list in hash for x in inner_list ]

    def __iter__(self):
        return self

    def next(self):
        return self.index[choice(self.hash)]

BONE = 'bone'
ENCT = 'encode_type'
MTXT = 'base_text'
ATCH = 'attachment'

class GenMsg(object):
    def __init__(self, configfile):
        fp=open(configfile,'r')
        self.cfg = yaml.load(fp.read())
        fp.close()

        self.atch_raw = {}
        self.atch_index = []
        self.atch_cache = {}
        self.bone_iter = BlackBox(self.cfg[BONE])
        self.enct_iter = BlackBox(self.cfg[ENCT])
        self.mtxt_iter = BlackBox(self.cfg[MTXT])
        self.atch_iter = BlackBox(self.cfg[ATCH])

        self.mtxt_files={}
        for key in self.cfg[MTXT].keys():
            fp = open('{0}/{1}'.format(self.cfg['filedir'],self.cfg[MTXT][key]['file']))
            self.mtxt_files[key] = fp.read()
            fp.close()

        self.atch_files = {}
        for key in self.cfg[ATCH].keys():
            fp = open('{0}/{1}'.format(self.cfg['filedir'],self.cfg[ATCH][key]['file']))
            self.atch_files[key] = fp.read()
            fp.close()


    def __iter__(self):
        return self

    def next(self):
        spec={}
        msg=None

        spec[BONE] = self.bone_iter.next()
        if self.cfg[BONE][spec[BONE]]['depth'] == 0:
            spec[ATCH] ={} 
            spec[MTXT] = self.mtxt_iter.next()
            spec[ENCT] = self.enct_iter.next()
            msg = self._plain( spec[MTXT], self.cfg[ENCT][spec[ENCT]]['charset'] )
        else:
            spec[ATCH] = [self.atch_iter.next() for x in range(self.cfg[BONE][spec[BONE]]['num_atch'])]
            spec[MTXT] ={} 
            spec[ENCT] = [self.enct_iter.next() for x in range(self.cfg[BONE][spec[BONE]]['num_atch'])]
            msg = self._multipart(self.cfg[BONE][spec[BONE]]['depth'], spec[ATCH], spec[ENCT])

        return ( msg.as_string(), spec )

    def _plain(self, text, encoding):
        msg = MIMEText(self.mtxt_files[text], 'plain', encoding)
        return msg

    def _multipart( self, depth, atchs, encts ):

        base_msg = MIMEMultipart()

        for atch_id, encode_type in zip(atchs, encts):
            ctypes, encoding = mimetypes.guess_type(self.cfg[ATCH][atch_id]['file'])
            if not ctypes or encoding:
                ctypes = 'application/octet-stream'
            maintype, subtype = ctypes.split('/', 1) 

            attach = MIMEBase(maintype, subtype)
            attach.set_payload(self.atch_files[atch_id])

            if encode_type == 'base64':
                encoders.encode_base64(attach)
            elif encode_type == 'qp':
                encoders.encode_quopri(attach)
            else:
                encoders.encode_7or8bit(attach)
            attach.add_header('Content-Disposition', 'attachment', filename=self.cfg[ATCH][atch_id]['file'])
            base_msg.attach(attach)

        outer=[]
        outer.append(base_msg)
        for i in range(depth):
            outer.append(MIMEMultipart())
            outer[-1].attach(outer[-2])
        return outer[-1]

if __name__ == '__main__':
    msgiter = GenMsg()
    for i in range(10):
        print msgiter.next()
