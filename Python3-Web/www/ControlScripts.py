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
    #update_user = User(name='梁启荣', email='114182222221@163.com', passwd='dhdhdhdh', image='about:xxxxxx', id='001493795043901eff6c32a8f7544218665cad2e7f6408500', admin='0', created_at='1490792489.37803') # 需要传入用户的id(主键), admin, created_at, 很不方便也许需要重构
    #await update_user.update()
    #printf(r)
    # => 
    # [{'admin': 0, 'password': '99998', 'name': 'sytu', 'created_at': 1490792489.37803, 'id': '001490793039689bb93e162417848c2823adf1909195208000', 'image': 'about:xxxxxx', 'email': 'imsytu@163.com'}]

    # attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)

    # 删除一位用户
    #remove_user = User(name='sytu', email='imsytu@163.com', password='9999', image='about:about', id='00149406394339574acb2ea6cba4ac4b12ea01d6f57fbf800') # 需要传入用户的id(主键)
    #await remove_user.remove()
    #r = await User.findall()
    # =>
    # []
    uid = '001494090483527f223fa4003384bc69da9c656d33d8e8500'
    uname = 'MARESFAC'
    uimage = 'http://www.gravatar.com/avatar/db9dd696ad73852995e891e5e0facbdc?d=mm@s=120'
    name = ['interesting', 'excited!', 'too young', 'too simple', 'sometimes naive', 'I\'m angry!']
    content = ['苟利国家生死以', '岂因祸福避趋之', '敢同恶鬼争高下', '不向霸王让存分','垂死病中惊坐起', '谈笑风生又一年']
    summary= ['吼哇!', '这是坠侯滴！', '不要见得风识得雨', '跑得比其他西方媒体还快', '一句话不说也不好', '我不是新闻工作者']
    for i, j, k in zip(name, content, summary):
        Bname, Bsummary, Bcontent = i, j, k
        blog = Blog(user_id=uid, user_name=uname, user_image=uimage, name=Bname, summary=Bsummary, content=Bcontent)
        r = await blog.save()
    r = await Blog.findall(orderBy='created_at desc')
    printf(r)
    await orm.destroy_pool()


loop.run_until_complete(test())  
loop.close()
if loop.is_closed():
    sys.exit(0)