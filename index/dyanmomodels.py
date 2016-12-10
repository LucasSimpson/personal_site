from django_dynamodb import BaseModel
from django_dynamodb import fields


class PriorWork(BaseModel):
    chrono_order = fields.HashKey(fields.NumberField())
    title = fields.RangeKey(fields.CharField())
    company = fields.CharField()
    dates = fields.CharField()
    location = fields.CharField()
    body = fields.CharField()
    img_url = fields.CharField()



