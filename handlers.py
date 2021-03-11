from aiohttp import web
import json


def root(request: web.Request):
    msg = 'root request'
    path = request.path
    body = json.dumps({'msg': msg,
                       'path': path})
    return web.Response(body=body, status=200)


def bla_bla_bla(request: web.Request):
    return web.Response(text='bla-bla-bla')
