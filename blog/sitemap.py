from django.contrib.sitemaps import Sitemap

from blog import BlogPost


class BlogListSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4

    def items(self):
        return []


class BlogPostsSitemap(Sitemap):
    # https://docs.djangoproject.com/en/2.2/ref/contrib/sitemaps/
    changefreq = "yearly"
    priority = 1.0

    def items(self):
        return BlogPost.all()

    def location(self, blog_post):
        return blog_post.get_absolute_url()

    def lastmod(self, blog_post):
        return blog_post.last_modified
