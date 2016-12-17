from django_dynamodb import BaseModel, fields, register_dynamodb_model


@register_dynamodb_model
class Interests(BaseModel):
    id = fields.HashNestedKey(fields.AutoIncrementingField())
    title = fields.RangeNestedKey(fields.CharField())
    url = fields.CharField()

