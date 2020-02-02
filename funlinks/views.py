from django.views.generic import TemplateView

from funlinks import FunLink
from utils.view_decorators import cache_control


class FunLinksListsView(TemplateView):
    template_name = 'fun_links/fun_links_list.html'

    @cache_control(4 * 60 * 60)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'fun_links': sorted(FunLink.all(), key=lambda link: -link.id)
        }

