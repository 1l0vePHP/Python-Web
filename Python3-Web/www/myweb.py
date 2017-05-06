#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import asyncio, os, inspect, logging, functools
from urllib import parse
from aiohttp import web
from apis import APIError

def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:   #关键字参数及默认参数为空
            args.append(name)
    return tuple(args)

def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:    #关键字参数
            args.append(name)
    return tuple(args)

def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:    #关键字参数
            return True

def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:    #可变长字典参数
            return True

def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_KEYWORD and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != ins):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found

class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)         #是否有request参数
        self._has_var_kw_arg = has_var_kw_arg(fn)           #是否有可变长字典参数
        self._has_named_kw_args = has_named_kw_args(fn)     #是否有关键字参数
        self._named_kw_args = get_named_kw_args(fn)         #所有关键字参数
        self._required_kw_args = get_required_kw_args(fn)   #所有没有默认值的关键字参数

    async def __call__(self, request):
        kw = None
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':    #如果是POST请求
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('appliction/x-www-form-urlencode') or ct.startswith('mutipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':    #如果是GET请求
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._named_kw_args:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args:' % k)
                kw[k] = v

        if self._has_request_arg:
            kw['request'] = request
        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)    #<<----------最终返回的值
            return r
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

"""
add_routes(app, module_name)
|
|-->handlers-->|
|              |-->>add_route(app,fn)->>|
|                                       |-->RequestHandler(app, fn)-->|
|                                                                     |
|<<--===================<URL Handler Function>====================<<--|

"""

def add_static(app):    #加载静态资源
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('static/', path))

def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path =getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get of @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

def add_routes(app, module_name):    #module_name = 'handlers'
    n = module_name.rfind('.')
    if n == (-1):
        #没有匹配才返回-1
        mod = __import__(module_name, globals(), locals())    #import handlers
    else:
        #z这里的else有意义吗??
        #返回.最后出现的位置索引
        name = module_name[n+1:]    #name为handlers模块里头的不同的URL处理函数，如果匹配成功的话，即index/create_conment/blog
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)    #此时mod为URL处理函数
    for attr in dir(mod):
        #过滤掉mod里以_开头的属性
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)    #handlers里的URL处理函数(handler_url_blog/handler_url_greeting/handler_url_input/handler_url_result/handler_url_index)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)