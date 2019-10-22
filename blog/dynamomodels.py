from django.urls import reverse
from django.utils import timezone

from blog.formatting.formatters import ToParagraphs, ToItalics, ToBold, Linkify, Formatter
from django_dynamodb import BaseModel, fields, register_dynamodb_model


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
        formatter = Formatter.chain([
            ToParagraphs(),
            ToItalics(),
            ToBold(),
            Linkify(),
        ])

        return formatter.format(self.content)

    def preview_as_html(self):
        formatter = Formatter.chain([
            ToParagraphs(2),
            ToItalics(),
            ToBold(),
            Linkify(),
        ])

        return formatter.format(self.content) + f'<p><a href="{self.get_absolute_url()}">Continue reading</a></p>'
