from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from funlinks import FunLink
from klu_pythonapi.notifications import push
from workexperience import WorkExperience


class KluView(TemplateView):
    """KLU Demo view. Just says some message, and pushes a KLU notification."""

    template_name = 'index/klu.html'

    def get_context_data(self, **kwargs):
        msg = kwargs.get('message', '')
        if msg:
            push('lucassimpson.com', 'Demo Success', msg)

        return {
            'message': msg
        }


class IndexView(TemplateView):
    """Main landing page."""

    template_name = 'index/index/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['fun_links'] = FunLink.all()
        return context


class WorkExperienceView(TemplateView):
    """Work experience page."""

    template_name = 'index/work_experience/work_experience.html'

    def get_context_data(self, **kwargs):
        context = super(WorkExperienceView, self).get_context_data(**kwargs)
        context['work_experiences'] = sorted(WorkExperience.all(), key=lambda we: -we.chrono_order)
        return context


class AboutView(TemplateView):
    """About me/site page."""

    template_name = 'index/about/about.html'


class ResumeRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return static('resume.pdf')


class RobotsRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return static('robots.txt')
