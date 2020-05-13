#!/usr/bin/env python3
#-*-coding:utf8-*-
import json
import requests
from ipabase import easylog

def send_dingding_msg(msg, access_token, timeout=5):
    headers = {
        'Content-Type': "application/json"
    }
    url = "https://oapi.dingtalk.com/robot/send"
    querystring = {"access_token":access_token}
    content = {
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    try:
        response = requests.post(url, data=json.dumps(content), headers=headers, params=querystring, timeout=timeout)
        easylog.info('dingding send message:%s %s', msg, response.text)
    except Exception as e:
        easylog.exception('dingding msg:%s', msg)