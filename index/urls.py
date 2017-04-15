from django.conf.urls import url

from .views import IndexView, KluView, WorkExperienceView, AboutView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^klu/(?P<message>.*)$', KluView.as_view(), name='klu'),
    url(r'^work_experience/$', WorkExperienceView.as_view(), name='work_experience'),
    url(r'^about/$', AboutView.as_view(), name='about'),
]