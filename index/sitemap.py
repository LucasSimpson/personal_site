from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class IndexSitemap(Sitemap):
    # https://docs.djangoproject.com/en/2.2/ref/contrib/sitemaps/
    changefreq = "yearly"
    priority = 0.8

    def items(self):
        return [
            'index',
            'work_experience',
            'about',
            'resume',
        ]

    def location(self, view_name):
        return reverse(f'index:{view_name}')
