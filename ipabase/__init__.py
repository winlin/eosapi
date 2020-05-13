# -*- coding: utf8 -*-

__version__ = '0.0.1'

__all__ = [
    'easylog',

    'IpaJsonEncoder',
    'object_method_time_usage',
    'time_usage',
    'random_str',
    'get_uuid_str',

    'send_dingding_msg'
]

from ipabase import easylog
from ipabase.comm import *
from ipabase.imsger import send_dingding_msg
