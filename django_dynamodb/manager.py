import logging

import boto3
from django.conf import settings


# dynamoDB table manager
class DynamoDBManager(object):
    instance = None

    @staticmethod
    def get_manager():
        if not DynamoDBManager.instance:
            DynamoDBManager.instance = DynamoDBManager()
        return DynamoDBManager.instance

    @staticmethod
    def get_table_name(cls):
        return '%s-%ss' % (DynamoDBManager.table_prefix, cls.__name__.lower())

    @staticmethod
    def _build_key_schema(cls):
        hash_key = cls.get_hash_key()
        range_key = cls.get_range_key()

        if hash_key is None:
            raise AttributeError('%s must have a HashKey defined' % cls)
        if range_key is None:
            raise AttributeError('%s must have a RangeKey defined' % cls)

        schema = [
            {
                'AttributeName': hash_key[2:],
                'KeyType': 'HASH'
            },
            {
                'AttributeName': range_key[2:],
                'KeyType': 'RANGE'
            }
        ]

        return schema

    @staticmethod
    def _build_attribute_schema(cls):
        hash_key = cls.get_hash_key()
        range_key = cls.get_range_key()

        if hash_key is None:
            raise AttributeError('%s must have a HashKey defined' % cls)
        if range_key is None:
            raise AttributeError('%s must have a RangeKey defined' % cls)

        schema = [
            {
                'AttributeName': hash_key[2:],
                'AttributeType': cls.__dict__[hash_key].get_proto()
            },
            {
                'AttributeName': range_key[2:],
                'AttributeType': cls.__dict__[range_key].get_proto()
            }
        ]

        return schema

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        dynamo_access_key = settings.DYNAMO_ACCESS_KEY
        dynamo_secret_access_key = settings.DYNAMO_SECRET_ACCESS_KEY
        DynamoDBManager.table_prefix = settings.DYNAMO_TABLE_PREFIX
        self._models = []

        self._conn = boto3.resource(
            'dynamodb',
            region_name='us-east-1',
            aws_access_key_id=dynamo_access_key,
            aws_secret_access_key=dynamo_secret_access_key)

    # creates a table for a given class
    def create_table(self, cls, read_units=1, write_units=1):
        # make table
        table_name = DynamoDBManager.get_table_name(cls)
        key_schema = DynamoDBManager._build_key_schema(cls)
        attribute_def = DynamoDBManager._build_attribute_schema(cls)
        table = self._conn.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_def,
            ProvisionedThroughput={
                'ReadCapacityUnits': read_units,
                'WriteCapacityUnits': write_units,
            }
        )

        # wait for it to be done
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    # returns the table of the given class
    def get_table(self, cls):
        table = self._conn.Table(DynamoDBManager.get_table_name(cls))
        return table

    # returns a list of all registered models
    def get_models(self):
        return self._models

    # register a model
    # TODO ignore duplicate registers
    def register_model(self, model):
        self.logger.info('registering %s' % model)
        self._models.append(model)