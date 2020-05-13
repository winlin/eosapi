#!/usr/bin/env python3
#-*-coding:utf8-*-
import os
import json
import time
import uuid
import string
import random
import base64
import datetime
from ipabase import easylog
from functools import wraps
from decimal import Decimal

class IpaJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, float) :
            return round(obj, 4)
        elif isinstance(obj, Decimal):
            return round(float(obj), 4)
        else:
            return json.JSONEncoder.default(self, obj)

def object_method_time_usage(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        easylog.debug('Begin %s.%s', self.__class__.__name__, method.__name__)
        start_point= time.time()
        method_rc = method(self, *args, **kwargs)
        easylog.info('End call %s.%s() FUNC TIME USAGE:%.3fs', self.__class__.__name__, method.__name__, time.time()-start_point)
        return method_rc
    return wrapper

def time_usage(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        easylog.debug('Begin %s', method.__name__)
        start_point= time.time()
        method_rc = method(*args, **kwargs)
        easylog.info('End %s() FUNC TIME USAGE:%.3fs', method.__name__, time.time()-start_point)
        return method_rc
    return wrapper

def random_str(length=8):
    '''Generate random string with specail length.
    The characters come from string.ascii_letters & string.digits
    '''
    population_str = string.ascii_letters + string.digits
    str_len = len(population_str)
    if length <= str_len:
        return ''.join(random.sample(population_str, length))
    times_int = length / str_len
    remainder_int = length % str_len
    max_random_str = ''.join(random.sample(population_str, str_len))
    return max_random_str * times_int + \
              ''.join(random.sample(population_str, remainder_int))

def get_uuid_str():
    '''Retrun guid string without '-'.'''
    return str(uuid.uuid4()).replace('-', '')

def b64encode(value):
    return None if value == None else base64.standard_b64encode(value)

def b64decode(value):
    return None if value == None else base64.standard_b64decode(value)

def check_dict_has_keys(dict_obj, keys):
    if dict_obj is None:
        return False
    for key in keys:
        if key not in dict_obj:
            return False
    return True

def read_json_conf(conf_path):
    if not os.path.exists(conf_path):
        return None
    sandbox_conf = {}
    with open(conf_path, 'r') as conf_f:
        sandbox_conf = json.loads(conf_f.read())
    return sandbox_conf

def obj_to_utf8_str(target_obj, cls=IpaJsonEncoder):
    value = target_obj
    if isinstance(value, (list, tuple, dict)):
        value = json.dumps(value, cls=cls)
    elif isinstance(value, unicode):
        value = value.encode('utf-8')
    return value

def datestr24h_2second(date_str):
    return int(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S")))

def second2_str24h(cur_second):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_second))



