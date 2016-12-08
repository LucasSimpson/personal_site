from django.views.generic import TemplateView


# landing page
class IndexView(TemplateView):
    template_name = 'index/index.html'


# work experience
class WorkExperienceView(TemplateView):
    template_name = 'work_experience/work_experience.html'