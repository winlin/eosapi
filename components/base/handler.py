#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import ujson as json
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
from ipabase import easylog,IpaJsonEncoder,second2_str24h,object_method_time_usage


class BaseHandler(RequestHandler):
    def initialize(self, *args):
        self.requestid = None

    @object_method_time_usage
    def render_json(self, data, requestid=False, jsonstr=False, indent=False):
        self.set_header('Content-Type', 'application/json')
        if jsonstr:
            data = json.loads(data)
        if requestid:
            data['requestid'] = 'requestid:%s midware_finish:%s' % (self.requestid, second2_str24h(time.time())[11:])

        try:
            data = json.dumps(data)
        except Exception as e:
            easylog.exception("%s data:%s", e, data)
            data = {'error':'JSON格式错误(%s)' % e}
            if requestid:
                data['requestid'] = 'requestid:%s midware_finish:%s' % (self.requestid, second2_str24h(time.time())[11:])
            data = json.dumps(data, cls=IpaJsonEncoder)
        try:
            start_time = time.time()
            self.write(data)
            easylog.info('write data length:%.02fKB TIME USAGE:%.4fs', len(data)/1024.0, time.time()-start_time)
        except Exception as e:
            easylog.critical('%s', e)

    async def fetch_info(self):
        http_client = AsyncHTTPClient()
        url = "%s/v1/chain/get_info" % (self.application.service_conf['eoshost'])
        try:
            result = await http_client.fetch(url)
            if result.code / 100 != 2:
                easylog.error("Failed to get_info error:%s", result.body)
                return None
            data = json.loads(result.body)
            return data
        except Exception as e:
            easylog.exception('block_num:%d %s', block_num, e)
        return None

    async def get_latest_info(self):
        now_ts = time.time()
        if now_ts - self.application.latest_block_info['ts'] < self.application.service_conf['get_info_sec'] + 0.1:
            return self.application.latest_block_info['info']
        info = await self.fetch_info()
        if info:
            self.application.latest_block_info['ts'], self.application.latest_block_info['info'] = time.time(), info
            return self.application.latest_block_info['info']
        return None
        
