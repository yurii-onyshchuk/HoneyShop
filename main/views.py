from django.views.generic import TemplateView


class Home(TemplateView):
    extra_context = {'title': 'Головна'}
    template_name = 'main/index.html'


class About(TemplateView):
    extra_context = {'title': 'Про нас'}
    template_name = 'main/about.html'


class Contact(TemplateView):
    extra_context = {'title': 'Контакти'}
    template_name = 'main/contact.html'
