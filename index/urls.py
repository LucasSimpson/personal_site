from django.conf.urls import url

from .views import IndexView, KluView, WorkExperienceView, AboutView, ResumeRedirectView, RobotsRedirectView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^klu/(?P<message>.*)$', KluView.as_view(), name='klu'),
    url(r'^work_experience/$', WorkExperienceView.as_view(), name='work_experience'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^resume/$', ResumeRedirectView.as_view(), name='resume'),
    url(r'^robots.txt', RobotsRedirectView.as_view(), name='robots'),
]