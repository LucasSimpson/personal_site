from django.views.generic import TemplateView

from funlinks import FunLink
from workexperience import WorkExperience


class IndexView(TemplateView):
    template_name = 'alt/index/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['fun_links'] = FunLink.all()
        return context


class WorkExperienceView(TemplateView):
    template_name = 'alt/work_experience/work_experience.html'

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceView, self).get_context_data(**kwargs)
        context['work_experiences'] = WorkExperience.all()
        return context