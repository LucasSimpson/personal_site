from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class BlogSitemap(Sitemap):
    # https://docs.djangoproject.com/en/2.2/ref/contrib/sitemaps/
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return [
            'posts-list',
            'social_arguer',
        ]

    def location(self, view_name):
        return reverse(f'blog:{view_name}')
