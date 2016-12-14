from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import WorkExperienceViewSet, FunLinkViewSet

router = routers.DefaultRouter()
router.register(r'work_experience', WorkExperienceViewSet, base_name='work_experience')
router.register(r'fun_links', FunLinkViewSet, base_name='fun_links')

urlpatterns = [
    # url(r'^$', IndexView.as_view(), name='index'),
    url('^', include(router.urls)),
]