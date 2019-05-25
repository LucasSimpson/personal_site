from django.views.generic import TemplateView


class PostsListsView(TemplateView):
    template_name = 'blog/posts-list.html'


class SocialArguerView(TemplateView):
    template_name = 'blog/posts/social_arguer.html'
