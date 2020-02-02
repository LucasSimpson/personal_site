from django.views.generic import TemplateView

from blog.dynamomodels import BlogPost
from utils.view_decorators import cache_control


class PostsListsView(TemplateView):
    template_name = 'blog/posts_list.html'

    @cache_control(4 * 60 * 60)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'posts': sorted(BlogPost.all(), key=lambda bp: -bp.date_created.timestamp())
        }


class PostDetailView(TemplateView):
    template_name = 'blog/post_detail.html'

    @cache_control(4 * 60 * 60)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        title = kwargs.get('title', None)

        for post in BlogPost.all():
            if post.url_title == title:
                return {
                    'post': post,
                }

        return {}
