"""PersonalSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from blog.sitemap import BlogSitemap
from index.sitemap import IndexSitemap

sitemaps = {
    'blog': BlogSitemap,
    'index': IndexSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^', include(('index.urls', 'index'), namespace='index')),
    url(r'^blog/', include(('blog.urls', 'blog'), namespace='blog')),
    url(r'^api/v1/', include(('api.urls', 'api'), namespace='api')),
]
