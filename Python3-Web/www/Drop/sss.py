from orm import Model, StringField, IntegerField

class User(Model):    #User与Mysql表的映射关系
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()

class Model(dict, metaclass=ModelMetaclass):
    
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mapping__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value
    
class Field(object):
    
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__)
    
class ModelMtaclass(type):
    
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
    
        tableName = attrs.get('__table__', None) or Name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if instance(v, Field):
                logging.info('found mapping: %s ==> %s' % (k,v))
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise RuntimeError('Douplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    field.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mapping.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))    #把fields里的元素全部用匿名函数lambda处理一遍
        attrs['__mapping__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ','.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ','.join(escaped_fields), primaryKey, creat_args_string(len(escaped_fields) + 1)
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ','.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields), primaryKey))
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primary)
        return type.__new__(cls, name, bases, attrs)