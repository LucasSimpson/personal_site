from django.conf.urls import url

from .views import IndexView, KluView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^klu/(?P<message>.*)$', KluView.as_view(), name='klu'),
]