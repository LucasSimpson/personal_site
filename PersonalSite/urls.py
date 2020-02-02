from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from blog.sitemap import BlogListSitemap, BlogPostsSitemap
from index.sitemap import IndexSitemap

sitemaps = {
    'blog_archive': BlogListSitemap,
    'blog_posts': BlogPostsSitemap,
    'index': IndexSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^', include(('index.urls', 'index'), namespace='index')),
    url(r'^blog/', include(('blog.urls', 'blog'), namespace='blog')),
    url(r'^links/', include(('funlinks.urls', 'fun_links'), namespace='fun_links')),
    url(r'^api/v1/', include(('api.urls', 'api'), namespace='api')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
