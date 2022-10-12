from django.views.generic import TemplateView


class Blog(TemplateView):
    template_name = 'blog/post_list.html'


class SinglePost(TemplateView):
    template_name = 'blog/post_detail.html'
