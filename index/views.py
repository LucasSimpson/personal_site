from django.views.generic import TemplateView

from klu_pythonapi.notifications import push


# landing page
class IndexView(TemplateView):
    template_name = 'index/index.html'


class KluView(TemplateView):
    """KLU Demo view. Just says some message, and pushes a KLU notification."""

    template_name = 'index/klu.html'

    def get_context_data(self, **kwargs):
        msg = kwargs.get('message', None)
        if msg:
            push('lucassimpson.com', 'Demo Success', msg)

        return {
            'message': kwargs.get('message', 'There is no message :(')
        }
