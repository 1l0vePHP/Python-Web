import asyncio
from aiohttp import web

async def handler_url_xxx(request):

    url_param = request.match_info['key']
    query_params = parse_qs(request.query_string)

    text = render('template', data)
return web.Response(text.encode('uft-8'))

def get(path):
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return wrapper

class RequsetHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn

    @asyncio.coroutine
    def __call__(self, reuqest):
        kw = 
        r = yield from self._func(**kw)
        return r