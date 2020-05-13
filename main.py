#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tornado
from tornado.options import define, options
from ipabase import easylog
from components.base.utils import start_httpserver

#############################################################################
# options
define("conf_file", help="the main.cfg file path", type=str)
define("address", default="127.0.0.1", help="listen address", type=str)
define("port", default=8899, help="listen port", type=int)
define("debug", default=False, help="enable debug mode", type=bool)
define("log_path", default=os.path.abspath(os.curdir), help="logging file path", type=str)
#############################################################################


def main():
    # remote debug
    # host: machine running Komodo or the DBGP Proxy (uses localhost if unspecified)
    # port: port to connect on (uses 9000 if unspecified)
    #brkOnExcept(host="192.168.1.141", port=9000)
    # Or you can use the command line to start the remote debuge
    # pydbgp -d 192.168.1.141:9000 ./main.py --port=8999 \
    #                                        --debug=True --logging=debug \
    #   --logging=debug|info|warning|error|none
    
    options.parse_command_line()
    easylog.setup("%s/nohup_%d.out" % (options.log_path,options.port), options.logging, log_file_enable=True, file_size_mb=20, file_count=2)
    
    handler_map = []
    # TODO: Here add your handlers before the DEFAULT handler_map
    from components.eosapi.hanlder import handler_map as eosapi_handler_map
    handler_map += eosapi_handler_map

    from components.default.handler import handler_map as default_handler_map
    handler_map += default_handler_map
    
    for h in handler_map:
        easylog.info(str(h))

    start_httpserver(handler_map, options)

#############################################################################
if __name__ == "__main__":
    main()
