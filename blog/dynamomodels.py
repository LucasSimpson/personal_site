from django_dynamodb import BaseModel, fields, register_dynamodb_model
from django.utils import timezone


@register_dynamodb_model
class BlogPost(BaseModel):
    id = fields.HashNestedKey(fields.AutoIncrementingField())
    date_created = fields.RangeNestedKey(fields.DateTimeField())
    last_modified = fields.DateTimeField()
    title = fields.CharField()
    content = fields.CharField()

    def save(self):
        self.last_modified = timezone.now()
        return super().save()
