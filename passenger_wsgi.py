# -*- coding: utf-8 -*-

import os
import sys
import web
from wecharInterface import WecharInterface

urls = (
    '/', 'WecharInterface'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

# class Hello:
#     def GET(self):
#         return "hi."

application = web.application(urls, globals()).wsgifunc()
