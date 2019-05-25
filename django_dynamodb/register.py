from .manager import DynamoDBManager


# reconfigures class attributes. also registers the class with DynamoDBManager
def register_dynamodb_model(cls):

    # rebind attributes accordingly
    for attr in list(cls.model_fields()):
        field = getattr(cls, attr)
        delattr(cls, attr)
        setattr(cls, '__%s' % attr, field)

    # register class
    manager = DynamoDBManager.get_manager()
    manager.register_model(cls)

    # return class
    return cls
