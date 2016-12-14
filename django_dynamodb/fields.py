

# fields hold no value. they are there purely for description, validation,
# and as an adapter between db storage and python rep
class ModelField(object):

    # proto is a string representing dynamoBD storage type, ex 'S'/'N'/'B'
    @classmethod
    def get_proto(cls):
        if hasattr(cls, 'proto'):
            return cls.proto

        raise NotImplemented('Subclass of ModelField must either declare proto value or override get_proto method')

    # called when class is first initialzed via new call, return an initial value if applicable
    # note this is NOT called when initialized from a DB call
    def init_value(self, instance, attr):
        return None

    # encode value from python -> db
    def encoded(self, value):
        raise NotImplemented('%s is a subclass of ModelField, and as such should implement \'encoded\' method.' % self.__class__)

    # decode value from db -> python
    def decoded(self, value):
        raise NotImplemented('%s is a subclass of ModelField, and as such should implement \'decoded\' method.' % self.__class__)

    # cast an input to corresponding type for comparisons. default pass-through
    def cast(self, value):
        return value


# generic Field that nests another field, delegates responsiblity to nested field
class NestedKeyField(ModelField):
    def __init__(self, nested_field):
        self._nested_field = nested_field

    def get_proto(self):
        return self._nested_field.get_proto()

    def init_value(self, instance, attr):
        return self._nested_field.init_value(instance, attr)

    def encoded(self, value):
        return self._nested_field.encoded(value)

    def decoded(self, value):
        return self._nested_field.decoded(value)

    def cast(self, value):
        return self._nested_field.cast(value)


# hash key
class HashNestedKey(NestedKeyField):
    pass


# range key
class RangeNestedKey(NestedKeyField):
    pass


# generic field for holding a number
class NumberField(ModelField):
    proto = 'N'

    def encoded(self, value):
        return int(value) if value is not None else None

    def decoded(self, value):
        return int(value) if value is not None else None

    def cast(self, value):
        return int(value)


# generic field for holding a string
class CharField(ModelField):
    proto = 'S'

    def encoded(self, value):
        return str(value) if value is not None else None

    def decoded(self, value):
        return str(value) if value is not None else None

    def cast(self, value):
        return str(value)


# number field that auto increments for each new item
# TODO performance issues aside, theres a bunch of concurrency issues here :( yaaayyy mvp
class AutoIncrementingField(NumberField):

    # TODO this terrible lmfao
    def init_value(self, instance, attr):
        # get all objects
        entries = instance.__class__.all()

        # get max value
        high = 0
        for entry in entries:
            id = getattr(entry, attr, 0)
            if id > high:
                high = id

        # return highest+1
        return high+1