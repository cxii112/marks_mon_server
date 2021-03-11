from aiohttp import web
import aiohttp_cors
from routes import routes
from settings import APPPORT

if __name__ == '__main__':
    app = web.Application()
    for route in routes:
        app.router.add_route(
            method=route.method,
            path=route.path,
            handler=route.handler,
            name=route.name
        )
    cors = aiohttp_cors.CorsConfig(app, defaults={
        '*': aiohttp_cors.ResourceOptions()
    })

    web.run_app(app, port=APPPORT)
