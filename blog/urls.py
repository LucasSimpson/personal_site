from django.conf.urls import url
from django.urls import path

from .views import PostsListsView, PostDetailView

urlpatterns = [
    url(r'^$', PostsListsView.as_view(), name='posts-list'),
    path('<slug:date>/<slug:title>/', PostDetailView.as_view(), name='post-detail'),
]