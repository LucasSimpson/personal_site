from django.conf.urls import url

from .views import IndexView, WorkExperienceView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^work_experience/$', WorkExperienceView.as_view(), name='work_experience')

]