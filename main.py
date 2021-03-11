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
        resource = cors.add(app.router.add_resource(route.path))
        cors.add(resource.add_route(route.method, route.handler))

    web.run_app(app, port=APPPORT)
