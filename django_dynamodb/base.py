from fields import HashKey, RangeKey, ModelField
from manager import DynamoDBManager

from .exceptions import ItemNotFoundException
from .queryset import QuerySet

# DynamoDB model
class BaseModel(object):
    isSet = False  # static hack :(

    # get all attributes of a class that are ModelFields subclasses
    @classmethod
    def model_fields(cls):
        for attr in cls.__dict__:
            if isinstance(cls.__dict__[attr], ModelField):
                yield attr

    # get the hash key attribute
    @classmethod
    def get_hash_key(cls):
        for attr in cls.model_fields():
            if isinstance(cls.__dict__[attr], HashKey):
                return attr

    # get the range key attribute
    @classmethod
    def get_range_key(cls):
        for attr in cls.model_fields():
            if isinstance(cls.__dict__[attr], RangeKey):
                return attr

    # rebind cls and self attributes. for each ModelField (name, instance) (n, mf):
    # delete cls[n]
    # set cls['__%s' % n] as mf
    # set self.[mf] as None, is now just a regular attribute user can set/get
    # note that we have to check to see if we have rebound on the class already..
    # theres def a better way of doing this tbh
    # TODO redisign this honestly it works but its kinda messy
    def __new__(cls, *args, **kwargs):
        instance = super(BaseModel, cls).__new__(cls, *args, **kwargs)

        for attr in list(cls.model_fields()):
            field = getattr(cls, attr)

            if cls.isSet:
                setattr(instance, attr[2:], None)
            else:
                delattr(cls, attr)
                setattr(cls, '__%s' % attr, field)
                setattr(instance, attr, None)

        if not cls.isSet:
            cls.isSet = True

        return instance

    def __init__(self):
        self.manager = DynamoDBManager.get_manager()
        self.table = self.manager.get_table(self.__class__)

    # get encoded representation of field's value. attr points too a ModelField instance
    # python -> db
    def encoded(self, attr):
        value = getattr(self, attr[2:])  # pull current value
        return getattr(self, attr).encoded(value)

    # set the value of a field from an encoded value. attr points too a ModelField instance
    # db -> python
    def decoded(self, attr, value):
        return getattr(self, attr).decoded(value)

    # save an item in dynamo
    def save(self):
        model_data = dict()
        for attr in self.__class__.model_fields():
            model_data[attr[2:]] = self.encoded(attr)

        print('calling save with %s' % model_data)
        self.table.put_item(Item=model_data)

    # delete item from dynamo :(
    def delete(self):
        hash_key = self.__class__.get_hash_key()
        range_key = self.__class__.get_range_key()
        hash_key_value = self.encoded(hash_key)
        range_key_value = self.encoded(range_key)

        key = {
            hash_key[2:]: hash_key_value,
            range_key[2:]: range_key_value
        }

        print('calling delete with key=%s' % key)
        self.table.delete_item(Key=key )

    # returns a queryset of all objects
    @classmethod
    def all(cls):
        return QuerySet(cls)

    # returns a single object form db based on hash key and range key
    # TODO optimize this lmfao
    @classmethod
    def get(cls, hash_key_value, range_key_value):
        hash_key = cls.get_hash_key()
        range_key = cls.get_range_key()

        for model in cls.all():
            if getattr(model, hash_key) == hash_key_value and getattr(model, range_key) == range_key_value:
                return model

        raise ItemNotFoundException('%s with (hash_key=%s, range_key=%s) wasn\'t found in dynamo' % (cls.__name__, hash_key_value, range_key_value))
