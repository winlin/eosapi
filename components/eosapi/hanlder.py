#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import ujson as json
import requests
import urllib
from ipabase import easylog
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
from components.base.handler import BaseHandler

def start_fetch_blockid(id_dict, conf_dict):
    id_dict_size = 3600
    last_clean_ts = 0
    while True:
        try:
            url = "%s/v1/chain/get_info" % (conf_dict['eoshost'])
            res = requests.get(url, timeout=3.0)
            if res.status_code / 100 != 2:
                easylog.error("Failed to get_info:%s", res.text)
                continue
            result = json.loads(res.text)
            if result['head_block_num'] in id_dict and result['head_block_id'] == id_dict[result['head_block_num']]['id']:
                continue
            easylog.info('%d : %s', result['head_block_num'], result['head_block_id'])
            id_dict[result['head_block_num']] = {'id':result['head_block_id'],'ts':time.time()}

            nums, now_ts = list(id_dict.keys()), time.time()
            if now_ts-last_clean_ts > id_dict_size/2 and len(nums)>id_dict_size:
                last_clean_ts = now_ts
                for key in nums:
                    if now_ts - id_dict[key]['ts'] > id_dict_size/2:
                        del id_dict[key]

        except Exception as e:
            easylog.exception("%s", e)
        finally:
            time.sleep(0.2)

class GetBlockIdHandler(BaseHandler):
    def initialize(self):
        super(GetBlockIdHandler, self).initialize()

    async def fetch_block(self, block_num):
        http_client = AsyncHTTPClient()
        body_params = '{"block_num_or_id":%d}' % (block_num)
        url = "%s/v1/chain/get_block" % (self.application.service_conf['eoshost'])
        try:
            result = await http_client.fetch(url, method="POST", body=body_params)
            if result.code / 100 != 2:
                easylog.error("Failed to get %d error:%s", block_num, result.text)
                return None
            data = json.loads(result.body)
            return data['id']
        except Exception as e:
            easylog.exception('block_num:%d %s', block_num, e)
        return None

    async def get(self):
        block_num = int(self.get_argument('block_num'))
        if block_num in self.application.local_cache:
            self.render_json(self.application.local_cache[block_num])
            return

        block_id = await self.fetch_block(block_num)
        if block_id:
            self.application.local_cache[block_num] = {'id':block_id,'ts':time.time()}
            self.render_json(self.application.local_cache[block_num])
            return
        self.render_json({"error":"retry again"})


    def head(self):
        self.set_header("Server", "XiaoNiuServer");

# base handler map
handler_map = [
    ('/get_blockid', GetBlockIdHandler),
]