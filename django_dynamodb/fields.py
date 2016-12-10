
class ModelField(object):

    @classmethod
    def get_proto(clz):
        if hasattr(clz, 'proto'):
            return clz.proto

        raise NotImplemented('Subclass of ModelField must either declare proto value or override get_proto method')

    def __init__(self):
        self.value = None

    def encoded(self):
        return self.value

    def decoded(self, value):
        return value


class KeyField(ModelField):
    def __init__(self, nested_field):
        self._nested_field = nested_field

    def get_proto(self):
        return self._nested_field.get_proto()

    def encoded(self):
        return self._nested_field.encoded()

    def decoded(self, value):
        return self._nested_field.decoded(value)


class HashKey(KeyField):
    pass


class RangeKey(KeyField):
    pass


class NumberField(ModelField):
    proto = 'N'

    def encoded(self):
        print('encoding number field, value is %s' % self.value)
        if self.value is not None:
            return int(self.value)
        else:
            return 0

    def decoded(self, value):
        if value is not None:
            return int(value)
        else:
            return None


class CharField(ModelField):
    proto = 'S'

    def encoded(self):
        if self.value is not None:
            return str(self.value)
        else:
            return 'null'

    def decoded(self, value):
        if value is not None:
            return str(value)
        else:
            return None
