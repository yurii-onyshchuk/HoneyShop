from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'main/index.html'


class About(TemplateView):
    template_name = 'main/about.html'


class Contact(TemplateView):
    template_name = 'main/contact.html'
