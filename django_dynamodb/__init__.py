from base import BaseModel

default_app_config = 'django_dynamodb.apps.DjangoDynamoDBConfig'


def register(model):
    from manager import DynamoDBManager
    manager = DynamoDBManager.get_manager()
    manager.register_model(model)

