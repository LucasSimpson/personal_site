from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import WorkExperienceViewSet, FunLinkViewSet, InterestsViewSet, BlogPostsViewSet

router = routers.DefaultRouter()
router.register(r'work_experience', WorkExperienceViewSet, base_name='work_experience')
router.register(r'fun_links', FunLinkViewSet, base_name='fun_links')
router.register(r'interests', InterestsViewSet, base_name='interests')
router.register(r'blog_posts', BlogPostsViewSet, base_name='blog_posts')

urlpatterns = [
    url('^', include(router.urls)),
]