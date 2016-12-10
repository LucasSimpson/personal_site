from fields import HashKey, RangeKey, ModelField
from manager import DynamoDBManager


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

    def _as_json(self):
        model_data = dict()
        for attr in self.__class__.model_attributes():
            model_data[attr] = getattr(self, attr)
        return model_data

    def save(self):
        self.table.put_item(Item=self._as_json())

    def delete(self):
        hash_key = self.__class__.get_hash_key()
        range_key = self.__class__.get_range_key()

        self.table.delete_item(
            Key={
                hash_key: getattr(self, hash_key),
                range_key: getattr(self, range_key)
            }
        )

    @classmethod
    def get(cls, hash_key_value, range_key_value):

        # build request
        hash_key = cls.get_hash_key()
        range_key = cls.get_range_key()
        key = {
                hash_key: hash_key_value,
                range_key: range_key_value
            }

        # make request
        response = DynamoDBManager.get_manager().get_table(cls).get_item(Key=key)

        # get item and rebind to self.__class__ item
        item_data = response['Item']
        model = cls()
        for key in item_data:
            setattr(model, key, item_data[key])
        return model
