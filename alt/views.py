from django.shortcuts import render

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'alt/index/index.html'


class WorkExperienceView(TemplateView):
    template_name = 'alt/index/index.html'