from django.shortcuts import render
from django.views.generic import TemplateView


class Blog(TemplateView):
    template_name = 'blog/blog_main_page.html'
