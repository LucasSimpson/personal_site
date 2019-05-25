from django.conf.urls import url

from .views import PostsListsView, SocialArguerView

urlpatterns = [
    url(r'^$', PostsListsView.as_view(), name='posts-list'),
    url(r'^2019-05-28/social_arguer/$', SocialArguerView.as_view(), name='social_arguer'),
]