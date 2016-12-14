from django_dynamodb import BaseModel, fields, register_dynamodb_model


@register_dynamodb_model
class FunLink(BaseModel):
    id = fields.HashNestedKey(fields.AutoIncrementingField())
    link = fields.RangeNestedKey(fields.CharField())
    title = fields.CharField()