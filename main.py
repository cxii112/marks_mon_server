from aiohttp import web
from routes import routes

if __name__ == '__main__':
    app = web.Application()
    for route in routes:
        app.router.add_route(
            method=route.method,
            path=route.path,
            handler=route.handler,
            name=route.name
        )
    web.run_app(app)
