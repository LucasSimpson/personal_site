import logging

from fields import HashNestedKey, RangeNestedKey, ModelField
from manager import DynamoDBManager
from .exceptions import ItemNotFoundException
from .queryset import QuerySet

logger = logging.getLogger(__name__)


# DynamoDB model
# TODO put all meta shit in _meta attribute of Meta class
# TODO get rid of all these loops and use dicts for lookup
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
            if isinstance(cls.__dict__[attr], HashNestedKey):
                return attr

    # get the range key attribute
    @classmethod
    def get_range_key(cls):
        for attr in cls.model_fields():
            if isinstance(cls.__dict__[attr], RangeNestedKey):
                return attr

    # given an attr (ex 'id') return the associated ModelField instance (ex instance of IntegerField)
    @classmethod
    def get_model_field(cls, field):
        for model_field in cls.model_fields():
            if model_field[2:] == field:
                return getattr(cls, model_field)
        return None

    def __init__(self, from_db=False):
        self.manager = DynamoDBManager.get_manager()
        self.table = self.manager.get_table(self.__class__)

        # set initial values (if any) according to field if not initialized from db
        # TODO replace with a create() method that internal methods call
        if not from_db:
            for attr in list(self.__class__.model_fields()):
                init_val = getattr(self.__class__, attr).init_value(self, attr[2:])
                setattr(self, attr[2:], init_val)

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

        logger.debug('Saving item to DB, Item=%s' % model_data)
        self.table.put_item(Item=model_data)

    # given a dictionary of {field: value} bind the data
    def bind(self, **data):
        for attr, value in data.items():
            field = self.__class__.get_model_field(attr)
            if field is not None:
                setattr(self, attr, field.cast(value))

    # given a dictionary of {field: value} bind and save the data
    def update(self, **data):
        self.bind(**data)
        self.save()

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

        logger.debug('Deleting item from DB, Key=%s' % key)
        self.table.delete_item(Key=key )

    # returns a queryset of all objects
    @classmethod
    def all(cls):
        return QuerySet(cls)

    # returns a single object form db based on hash key and range key
    # TODO optimize this lmfao
    # TODO move to object manager
    # TODO return queryset?
    @classmethod
    def get(cls, hash_key_value, range_key_value):
        hash_key = cls.get_hash_key()[2:]
        range_key = cls.get_range_key()[2:]

        for model in cls.all():
            if getattr(model, hash_key) == hash_key_value and getattr(model, range_key) == range_key_value:
                return model

        raise ItemNotFoundException('%s with (hash_key=%s, range_key=%s) wasn\'t found in dynamo' % (cls.__name__, hash_key_value, range_key_value))

    # returns all objects matching the hash key
    # TODO optimize this lmfao
    # TODO move to object manager
    # TODO return queryset?
    @classmethod
    def filter_hashkey(cls, hash_key_value):
        hash_key = cls.get_hash_key()[2:]
        models = []
        for model in cls.all():
            if getattr(model, hash_key) == hash_key_value:
                models.append(model)

        return models
