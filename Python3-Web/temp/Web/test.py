'''from inspect import signature
def typeassert(*ty_args,**ty_kargs):
    def decorator(func):
        #func ->a,b
        #d = {'a':int,'b':str}
        sig = signature(func)
        btypes = sig.bind_partial(*ty_args,**ty_kargs).arguments
        print('btypes:')
        print(btypes)
        def wrapper(*args,**kargs):
            #arg in d,instance(arg,d[arg])
            print('sig.bind(xxx).arguments:')
            print(sig.bind(*ty_args,**ty_kargs).arguments)
            for name, obj in sig.bind(*ty_args,**ty_kargs).arguments:
                if name in btypes:
                    if not instance(obj,btyes[name]):
                        raise TypeError('"%s" must be "%s"' %(name,btyes[name]))

            return func(*args,**kargs)
        return wrapper
    return decorator

@typeassert(int,str,list)
def f(a,b,c):
    print(a,b,c)

if __name__ == '__main__':
    f(12, 'fawe', [1,2,3])'''

#def add_routes(app, module_name):
def add_routes(module_name):
    n = module_name.rfind('.')
    print('n:', n)
    if n == (-1):
        #没有匹配才返回-1
        mod = __import__(module_name, globals(), locals())
        print('mod:', mod)
    else:
        #返回.最后出现的位置索引
        name = module_name[n+1:]    #name为handlers模块里头的不同的URL处理函数，如果匹配成功的话，即index/create_conment/blog
        print('name:', name)
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)    #此时mod为URL处理函数
        print('mod:', mod)
    for attr in dir(mod):
        #过滤掉[name]函数里以_开头的属性
        print('attr:', attr)
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        print('fn:', fn)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                #add_route(app, fn)
                pass


add_routes('handlers.handler_url_index')