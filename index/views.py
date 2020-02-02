from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from blog import BlogPost
from funlinks import FunLink
from klu_pythonapi.notifications import push
from utils.view_decorators import cache_control
from workexperience import WorkExperience


class KluView(TemplateView):
    """KLU Demo view. Just says some message, and pushes a KLU notification."""

    template_name = 'index/klu.html'

    # disabling cause this is public and I don't want y'all spamming the HELL outta this

    # def get_context_data(self, **kwargs):
    #     msg = kwargs.get('message', '')
    #     if msg:
    #         push('lucassimpson.com', 'Demo Success', msg)
    #
    #     return {
    #         'message': msg
    #     }


class IndexView(TemplateView):
    """Main landing page."""

    template_name = 'index/index/index.html'

    @cache_control(4 * 60 * 60)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'blog_posts': list(sorted(BlogPost.all(), key=lambda bp: -bp.date_created.timestamp()))[:5]
        }


class AboutView(TemplateView):
    """About me/site page."""

    template_name = 'index/about/about.html'

    @cache_control(4 * 60 * 60)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ResumeRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return static('resume.pdf')


class RobotsRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return static('robots.txt')
