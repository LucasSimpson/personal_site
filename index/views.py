from django.views.generic import TemplateView


# landing page
class IndexView(TemplateView):
    template_name = 'index/index.html'
