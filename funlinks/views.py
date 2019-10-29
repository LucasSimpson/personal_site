from django.views.generic import TemplateView

from funlinks import FunLink


class FunLinksListsView(TemplateView):
    template_name = 'fun_links/fun_links_list.html'

    def get_context_data(self, **kwargs):
        return {
            'fun_links': sorted(FunLink.all(), key=lambda link: -link.id)
        }

