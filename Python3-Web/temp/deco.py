#!/usr/bin/env python

from time import time, sleep, ctime

def logged(when):
    def log(f, *args, **kargs):
        print('''Called:
        function: %s
        args: %r
        kargs: %r''' % (f, args, kargs))
    
    def pre_logged(f):
        def wrapper(*args, **kargs):
            log(f, *args, **kargs)
            sleep(3)
            print('pre time: %s || pre position: %s' % (ctime(), id(f)))
            return f(*args, **kargs)
        return wrapper
    
    def post_logged(f):
        def wrapper(*args, **kargs):
            now = time()
            try:
                return f(*args, *kargs)
            finally:
                sleep(3)
                print('post time: %s || post position: %s' % (ctime(), id(f)))
                log(f, *args, **kargs)
                print("time delta: %s" % (time()-now))
        return wrapper
    print('Why ???', when)
    print('I need Know whyyy!!!', when)
    try:
        print('logged time: %s' % ctime())
        return {"pre": pre_logged, "post": post_logged}[when]
    except KeyError as e:
        raise (ValueError(e), 'must be "pre" or "post"')

@logged("pre")
def hello(name):
    print("Hello,", name)

@logged("post")
def hello1(name):
    print("Hello,", name)
hello("World!")
sleep(2)
print('middle')
sleep(2)
hello1("closure!!")