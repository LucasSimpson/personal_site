from django.conf.urls import url, include

from rest_framework import routers

from .viewsets import PriorWorkViewSet

router = routers.DefaultRouter()
router.register(r'prior_work', PriorWorkViewSet, base_name='prior_work')

urlpatterns = [
    # url(r'^$', IndexView.as_view(), name='index'),
    url('^', include(router.urls)),
]