#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
from tornado.web import RequestHandler
from components.base.handler import BaseHandler


class PageNotFoundHandler(RequestHandler):
    def dobusiness(self):
        self.set_header('Content-Type', 'application/json')
        self.write('{"error":"Not suppoerted method"}')

    def get(self):
        self.dobusiness()
    def post(self):
        self.dobusiness()
    def delete(self):
        self.dobusiness()
    def put(self):
        self.dobusiness()
    def head(self):
        self.dobusiness()

class EchoHandler(BaseHandler):
    def initialize(self):
        super(EchoHandler, self).initialize()

    def get(self):
        self.write('%s'%time.time())

    def head(self):
        self.set_header("Server", "XiaoNiuServer");

# base handler map
handler_map = [
    ('/echo', EchoHandler),
    ('.*', PageNotFoundHandler),
]