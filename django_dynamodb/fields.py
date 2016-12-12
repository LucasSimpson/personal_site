

# fields hold no value. they are there purely for description, validation,
# and as an adapter between db storage and python rep
class ModelField(object):

    # proto is a string representing dynamoBD storage type, ex 'S'/'N'/'B'
    @classmethod
    def get_proto(cls):
        if hasattr(cls, 'proto'):
            return cls.proto

        raise NotImplemented('Subclass of ModelField must either declare proto value or override get_proto method')

    # encode value from python -> db
    def encoded(self, value):
        raise NotImplemented('%s is a subclass of ModelField, and as such should implement \'encoded\' method.' % self.__class__)

    # decode value from db -> python
    def decoded(self, value):
        raise NotImplemented('%s is a subclass of ModelField, and as such should implement \'decoded\' method.' % self.__class__)


class KeyField(ModelField):
    def __init__(self, nested_field):
        self._nested_field = nested_field

    def get_proto(self):
        return self._nested_field.get_proto()

    def encoded(self, value):
        return self._nested_field.encoded(value)

    def decoded(self, value):
        return self._nested_field.decoded(value)


class HashKey(KeyField):
    pass


class RangeKey(KeyField):
    pass


class NumberField(ModelField):
    proto = 'N'

    def encoded(self, value):
        return int(value) if value is not None else None

    def decoded(self, value):
        return int(value) if value is not None else None


class CharField(ModelField):
    proto = 'S'

    def encoded(self, value):
        return str(value) if value is not None else None

    def decoded(self, value):
        return str(value) if value is not None else None
