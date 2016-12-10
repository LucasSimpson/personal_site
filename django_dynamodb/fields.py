
class ModelField(object):

    @classmethod
    def get_proto(clz):
        if hasattr(clz, 'proto'):
            return clz.proto

        raise NotImplemented('Subclass of ModelField must either declare proto value or override get_proto method')

    def __init__(self):
        self.value = None


class KeyField(ModelField):
    def __init__(self, field_type):
        self._field_type = field_type

    def get_proto(self):
        return self._field_type.get_proto()


class HashKey(KeyField):
    pass


class RangeKey(KeyField):
    pass


class NumberField(ModelField):
    proto = 'N'


class CharField(ModelField):
    proto = 'S'
