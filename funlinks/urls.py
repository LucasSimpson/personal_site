from django.conf.urls import url

from .views import FunLinksListsView

urlpatterns = [
    url(r'^$', FunLinksListsView.as_view(), name='fun-links-list'),
]
