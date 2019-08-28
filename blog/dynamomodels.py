from django.urls import reverse

import re
from django_dynamodb import BaseModel, fields, register_dynamodb_model
from django.utils import timezone


def create_formatter(deliminator, html_tag):
    def replace(match):
        og = match.group(0)
        t1 = og[0]
        tn = og[-1]
        return f'{t1}<{html_tag}>{og[2:-2]}</{html_tag}>{tn}'

    def formatter(text):
        return re.sub(r'[^a-zA-Z0-9]' + deliminator + r'[^.]+?' + deliminator + r'[^a-zA-Z0-9]', replace, text)

    return formatter


italics = create_formatter(r'_', 'i')
bold = create_formatter(r'\*', 'b')


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

    def date_string(self):
        return self.date_created.strftime("%b %d %Y")

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
        paragraphs = self.content.split('  ')
        html = ''
        for para in paragraphs:
            html += f'<p>{para}</p>'

        return bold(italics(html))
