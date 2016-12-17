from django_dynamodb import BaseModel, fields, register_dynamodb_model


@register_dynamodb_model
class WorkExperience(BaseModel):
    id = fields.HashNestedKey(fields.AutoIncrementingField())
    chrono_order = fields.NumberField()
    title = fields.RangeNestedKey(fields.CharField())
    company = fields.CharField()
    dates = fields.CharField()
    location = fields.CharField()
    body = fields.CharField()
    img_url = fields.CharField()
    rich_img_url = fields.CharField()



