import handlers
from utils import Route
from weeks import routes as weeks_routes

# routes = []
routes = [
    Route(
        method='GET',
        path='/',
        handler=handlers.root,
        name='root')
]
#     Route(
#         method='GET',
#         path='/bla-bla-bla',
#         handler=handlers.bla_bla_bla,
#         name='bla_bla_bla',
#         description='return bla-bla-bla string'),
# ]

routes += weeks_routes
