from aiohttp import web
import aiohttp_cors
from routes import routes
from settings import APPPORT

if __name__ == '__main__':
    app = web.Application()
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in routes:
        app.router.add_route(method=route.method,
                             path=route.path,
                             name=route.name,
                             handler=route.handler)
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, port=APPPORT)
