from aiohttp import web
import json


def root(request: web.Request):

    return web.Response(status=200)


def bla_bla_bla(request: web.Request):
    return web.Response(text='bla-bla-bla')
