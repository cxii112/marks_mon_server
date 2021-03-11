from utils import Route
from . import handlers
from .conf import api_prefix as prefix
from .conf import api_prefix_v1 as v1

routes_v1 = [
    Route(
        method='GET',
        path=f'{prefix}/{v1}/get/',
        handler=handlers.v1.get,
        name=f'{v1}_get'),
    Route(
        method='POST',
        path=f'{prefix}/{v1}/create/',
        handler=handlers.v1.create,
        name=f'{v1}_create'),
]
