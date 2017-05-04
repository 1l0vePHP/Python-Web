#!/usr/bin/env python
# -*-coding: utf-8 -*-

import orm, asyncio, sys
from models import User, Blog, Comment
from aiohttp import web
from time import ctime

#打印每个用户的个人信息
'''def printf(result):
    border = '*' * 80
    for i in result:
        print(border)
        for name in i.keys():
            if name == 'created_at':
                Dictvl = ctime(i[name])
                star = pstars(name, Dictvl)
                print('%s: %s' % (name, star))
            elif type(i[name]).__name__ == 'int':
                length = 76 - len(name)
                star = ' ' * length + '*'
                print('%s: %s%s' % (name, i[name], star))
            else:
                Dictvl = i[name]
                star = pstars(name, Dictvl)
                print('%s: %s' % (name, star))
    print(border)

def pstars(name, namevalue):
    length = 77 - len(name) - len(namevalue)
    revalue = namevalue + ' ' * length + '*'
    return revalue'''

def printf(result):
    blen = 80
    border = '*' * blen
    for i in result:
        print(border)
        for key in i.keys():
            ps = printstars(key, i[key], blen)
            print('%s: %s%s' % ps)
    print(border)

def printstars(key, value, blen=80):    #value等于i[name]
    __doc__ == 'v1.1.0'
    if type(value).__name__ == 'int':
        vlen = len(str(value))        #使int变字符串得到长度
    elif key == 'created_at':
        value = ctime(value)
        vlen = len(value)
    else:
        vlen = len(value)
    tlen = blen - len(key) - vlen - 3
    star = ' ' * tlen + '*'
    return (key, value, star)

loop = asyncio.get_event_loop()  


#创建实例
async def test():
    await orm.create_pool(loop=loop, host='localhost', port=3306, user='root', password='GLGJSSY817', db='test')

    # 创建一位用户:
    #new_user = User(name='bigfoot', email='114183201@qq.com', passwd='0123456789', image='about:about')
    #await new_user.save()
    #r = await User.findall()
    #print(r)
    # =>
    # [{'created_at': 1490792489.37803, 'password': '123456', 'id': '001490793039689bb93e162417848c2823adf1909195208000', 'email': 'imsytu@163.com', 'admin': 0, 'image': 'about:about', 'name': 'sytu'}]

    # 修改一位用户:
    #update_user = User(name='梁启荣', email='114183201@163.com', passwd='dhdhdhdh', image='about:xxxxxx', id='001493795043901eff6c32a8f7544218665cad2e7f6408500', admin='0', created_at='1490792489.37803') # 需要传入用户的id(主键), admin, created_at, 很不方便也许需要重构
    #await update_user.update()
    #r = await User.findall()
    #print(r)
    # => 
    # [{'admin': 0, 'password': '99998', 'name': 'sytu', 'created_at': 1490792489.37803, 'id': '001490793039689bb93e162417848c2823adf1909195208000', 'image': 'about:xxxxxx', 'email': 'imsytu@163.com'}]

    # attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)

    # 删除一位用户
    remove_user = User(name='sytu', email='imsytu@163.com', password='9999', image='about:about', id='001493479176167811be24babf54d178d485aa5cb86773a00') # 需要传入用户的id(主键)
    await remove_user.remove()
    r = await User.findall()
    printf(r)
    # =>
    # []

    await orm.destroy_pool()


loop.run_until_complete(test())  
loop.close()
if loop.is_closed():
    sys.exit(0)