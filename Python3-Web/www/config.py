#!/usr/bin/env python

import config_default

class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    #扫描configs里头的字典，把键值对全部找出来用Dict这个自建的dict派生出来的类替换，总共递归一次即'db'和'session'的值也是dict类，全部替换成Dict类
    for k, v in d.items():
        #print('k: %s v: %s' % (k, v))
        D[k] = toDict(v) if isinstance(v, dict) else v
        #print('D', D)
    #print('Return D:', D)
    #结果使得configs类型由dict变为Dict类，包括其内部'db'的值{'host': xxx, 'port': xx}类型也由dic类变为Dict类，从而具有句点属性
    #即configs['db'] = {xxxxxx} <==> configs.db = {xxxxxx}, db.host <==> db['host'], db.port <==> db['port']
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)
'''
print('configs.db: %s configs.session: %s' % (configs.db, configs.session))
a = configs.db; b = configs.session
print('configs.db.host: %s configs.session.secret: %s' % (a.host, b.secret))'''