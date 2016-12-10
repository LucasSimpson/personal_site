from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand

from django_dynamodb.manager import DynamoDBManager


class Command(BaseCommand):
    help = 'Creates all tables in DynamoDB'

    def handle(self, *args, **options):
        manager = DynamoDBManager.get_manager()
        models = manager.get_models()

        for model in models:
            table_name = manager.get_table_name(model)
            try:
                manager.create_table(model)
                self.stdout.write(self.style.SUCCESS('%s created...' % table_name))
            except ClientError:
                self.stdout.write('%s table already exists...' % table_name)

        self.stdout.write(self.style.SUCCESS('All tables created.'))
