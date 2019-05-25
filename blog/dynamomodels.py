from django_dynamodb import BaseModel, fields, register_dynamodb_model
from django.utils import timezone


@register_dynamodb_model
class BlogPost(BaseModel):
    id = fields.HashNestedKey(fields.AutoIncrementingField())
    date_created = fields.RangeNestedKey(fields.DateTimeField())
    last_modified = fields.DateTimeField()
    url_title = fields.CharField()
    title = fields.CharField()
    content = fields.CharField()

    def save(self):
        self.last_modified = timezone.now()
        return super().save()

    def get_url_title(self):
        return self.url_title

    def get_url_date(self):
        return f'{self.date_created.year}-{self.date_created.month}-{self.date_created.day}'

    def content_as_html(self):

        def parse_for_italics(text):
            result = ''
            words = text.split(' ')

            for w in words:
                if len(w) > 2 and w[0] == '_' and w[-1] == '_':
                    nested = parse_for_italics(w[1:-1])
                    result += f' <i>{nested}</i>'
                else:
                    result += f' {w}'

            return result

        content = self.content
        paragraphs = content.split('  ')

        html = ''

        for para in paragraphs:
            formatted = parse_for_italics(para)
            html += f'<p>{formatted}</p>'

        return html
