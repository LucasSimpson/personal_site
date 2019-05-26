from django.urls import reverse

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
        m = str(self.date_created.month)
        if len(m) == 1:
            m = f'0{m}'

        d = str(self.date_created.day)
        if len(d) == 1:
            d = f'0{d}'

        return f'{self.date_created.year}-{m}-{d}'

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'title': self.get_url_title(), 'date': self.get_url_date()})

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
