# -*- coding: utf-8 -*-

from logging import getLogger
module_logger = getLogger(__name__)

import sys
import re
import json
import httplib, urllib

class PoorInfluxDBClient(object):
    def __init__(self,
                 host='localhost',
                 port='localhost',
                 username='root',
                 password='root',
                 database=None,
                 time_precision='s',
                 timeout=10,
                 force=False):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self._timeout = timeout
        self._time_precision = time_precision
        self.regx_into = re.compile('\s+into\s+(\S+)')
        self.force = force

        module_logger.debug('Initialize:host={0}:port={1}:database={2}'.format(host,port,database))

        self._headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain'}
        if force and not self._database in [x['name'] for x in self.db_get()]:
            self.db_put(self._database)


    def write_points(self,dict_data):
        params = urllib.urlencode({'u': self._username, 'p': self._password, 'time_precision':self._time_precision})
        conn=httplib.HTTPConnection(self._host, self._port, timeout=self._timeout)
        post_data=json.dumps(dict_data)
        r1 = conn.request('POST','/db/{0}/series?{1}'.format(self._database, params), post_data, self._headers)
        module_logger.debug('ConnRequest:return={0}'.format(r1))
        r2 = conn.getresponse()
        try:
            module_logger.info('POST:name=[{0}]:len=[{1}]:status=[{2}]:reason=[{3}]'.format(dict_data[0]['name'],len(dict_data[0]['points']),r2.status,r2.reason))
            module_logger.debug('POSTResponseMsg:msg=[{0}]'.format('{0}'.format(r2.msg).replace('\n','\\n').replace('\r','\\r')))
            if r2.reason != 'OK':
                module_logger.debug('ResponseBad:[{0}]'.format(dict_data))
        except Exception, e:
            module_logger.error('FailedPostToInfluxDB:error=[{0}]:status=[{1}]:reason=[{2}]'.format(e, r2.status, r2.reason))
            conn.close()
            sys.exit(-1)
        conn.close()

    def db_put(self, dbname ):
        params =  urllib.urlencode({'u': self._username, 'p': self._password, 'time_precision':self._time_precision })
        conn=httplib.HTTPConnection(self._host, self._port, timeout=self._timeout)
        r1 = conn.request('POST','/db?{0}'.format(params), '{{ "name": "{0}" }}'.format(dbname) )
        r2 = conn.getresponse()
        return


    def db_get(self):
        params =  urllib.urlencode({'u': self._username, 'p': self._password, 'time_precision':self._time_precision })
        conn=httplib.HTTPConnection(self._host, self._port, timeout=self._timeout)
        tmp_url='/db?{0}'.format(params)
        r1 = conn.request('GET',tmp_url)
        r2 = conn.getresponse()
        try:
            module_logger.debug('GET:status=[{0}]:reason=[{1}]:url=[{2}]'.format(r2.status, r2.reason,tmp_url))
            contents = json.loads(r2.read())
        except Exception, e:
            conn.close()
            module_logger.error('FailedGetFromInfluxDB:error=[{0}]:status=[{1}]:reason=[{2}]:url=[{3}]'.format(e, r2.status, r2.reason, tmp_url))
            sys.exit(-1)
        conn.close()
        return contents

    def store_query(self, query):
        regx_result = self.regx_into.search(query)
        if not regx_result:
             module_logger.error('InvalidContinuousQuery:query=[{0}]'.format(query))
        raw_q_list = self.query('list continuous queries')[0]
        regx_results = [ self.regx_into.search(q[raw_q_list['columns'].index('query')]) for q in raw_q_list['points']]
        regx_results_ids = [ int(q[raw_q_list['columns'].index('id')]) for q in raw_q_list['points']]
        if regx_result.group(1) in [ x.group(1) if x  else '' for x in regx_results]:
            if not self.force:
                return
            self.query('drop continuous query {0}'.format(regx_results_ids[[ x.group(1) if x  else '' for x in regx_results].index(regx_result.group(1))]))
        self.query(query)
        return


    def query(self, query):
        params = urllib.urlencode({'u': self._username, 'p': self._password, 'q':query, 'time_precision':self._time_precision })
        conn=httplib.HTTPConnection(self._host, self._port, timeout=self._timeout)
        tmp_url='/db/{0}/series?{1}'.format(self._database, params)
        r1 =  conn.request('GET',tmp_url, "",self._headers)
        r2 = conn.getresponse()
        try:
            module_logger.debug('GET:status=[{0}]:reason=[{1}]:url=[{2}]'.format(r2.status, r2.reason,tmp_url))
            contents = json.loads(r2.read())
        except Exception, e:
            conn.close()
            module_logger.error('FailedGetFromInfluxDB:error=[{0}]:status=[{1}]:reason=[{2}]:url=[{3}]'.format(e, r2.status, r2.reason, tmp_url))
            sys.exit(-1)
        conn.close()
        return contents

    def get_list_series(self):
        raw_response = self.query('list series')
        module_logger.debug('Response:data={0}'.format(raw_response))

        return raw_response

    def csv_get(self,query, delimit=','):
        return self._convert_dict_to_csv( self.query(query), delimit )

    def csv_dbget(self):
        return  self._convert_dbs_to_csv(self.db_get() )

    def _convert_dict_to_csv(self, response, delimit=','):
        import datetime as dt
        if response[0]['points']:
            rslt_list =  [delimit.join([column for column in response[0]['columns'] ])]+[ delimit.join([ str(x) if i != response[0]['columns'].index('time') else dt.datetime.fromtimestamp(x).strftime('%Y-%m-%dT%H:%M:%S') for i,x in enumerate(row)]) for row in response[0]['points'] ]
            return '\n'.join(rslt_list)
        else:
            return delimit.join([column for column in response[0]['columns'] ])

    def _convert_dbs_to_csv(self, response, delimit=','):
        if response:
            return '\n'.join([row['name'] for row in response])


