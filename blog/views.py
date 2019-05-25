from django.views.generic import TemplateView

from blog.dynamomodels import BlogPost


class PostsListsView(TemplateView):
    template_name = 'blog/posts_list.html'

    def get_context_data(self, **kwargs):
        return {
            'posts': BlogPost.all()
        }


class PostDetailView(TemplateView):
    template_name = 'blog/posts_detail.html'

    def get_context_data(self, **kwargs):
        title = kwargs.get('title', None)

        for post in BlogPost.all():
            if post.url_title == title:
                return {
                    'post': post,
                }

        return {}
