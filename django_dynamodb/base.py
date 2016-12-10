from fields import HashKey, RangeKey, ModelField
from manager import DynamoDBManager

from .exceptions import ItemNotFoundException

# DynamoDB model
class BaseModel(object):

    # get all attributes that are ModelFields
    @classmethod
    def model_attributes(cls):
        for attr in cls.__dict__:
            if isinstance(cls.__dict__[attr], ModelField):
                yield attr

    # get the hash key attribute
    @classmethod
    def get_hash_key(cls):
        for attr in cls.model_attributes():
            if isinstance(cls.__dict__[attr], HashKey):
                return attr

    # get the range key attribute
    @classmethod
    def get_range_key(cls):
        for attr in cls.model_attributes():
            if isinstance(cls.__dict__[attr], RangeKey):
                return attr

    def __init__(self):
        self.manager = DynamoDBManager.get_manager()
        self.table = self.manager.get_table(self.__class__)

        # decorate all modelFields with getters/setters
        for attr in self.__class__.model_attributes():

            model_field = self.__class__.__dict__[attr]
            setattr(self, '__%s' % attr, model_field)

            def getter(s):
                return model_field.value
            def setter(s, value):
                model_field.value = value
            setattr(self, attr, property(getter, setter))

    # get encoded representation of field's value
    def encoded(self, attr):
        return getattr(self, '__%s' % attr).encoded()

    # set the value of a field from an encoded value
    def decoded(self, attr, value):
        return getattr(self, '__%s' % attr).decoded(value)

    # save an item in dynamo
    def save(self):
        print(self.__dict__)
        print(self.chrono_order)
        model_data = dict()
        for attr in self.__class__.model_attributes():
            model_data[attr] = self.encoded(attr)

        print('calling save with %s' % model_data)
        self.table.put_item(Item=model_data)

    # delete item from dynamo :(
    def delete(self):
        hash_key = self.__class__.get_hash_key()
        range_key = self.__class__.get_range_key()
        hash_key_value = self.encoded(hash_key)
        range_key_value = self.encoded(range_key)
        self.table.delete_item(
            Key={
                hash_key: getattr(self, hash_key_value),
                range_key: getattr(self, range_key_value)
            }
        )

    # returns an iterator containing all objects db
    # TODO make this lazy AF
    @classmethod
    def all(cls):
        table = DynamoDBManager.get_manager().get_table(cls)
        response = table.scan()

        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        models = list()
        for datum in data:
            model = cls()
            for key in datum:
                value = datum[key]
                decoded = model.decoded(key, value)
                setattr(model, key, decoded)
            models.append(model)

        return models

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
