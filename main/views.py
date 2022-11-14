from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.contrib import messages


class Home(TemplateView):
    extra_context = {'title': 'Головна'}
    template_name = 'main/index.html'


class About(TemplateView):
    extra_context = {'title': 'Про нас'}
    template_name = 'main/about.html'


class Contact(FormView):
    extra_context = {'title': 'Контакти'}
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.first_name
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        context = {'name': form.cleaned_data['name'],
                   'email': form.cleaned_data['email'],
                   'message': form.cleaned_data['message'],
                   }
        html_message = get_template('main/contact_form_message.html').render(context)
        send_mail(subject="Повідомлення з форми зворотнього зв'язку",
                  from_email=form.cleaned_data['email'],
                  recipient_list=[settings.EMAIL_HOST_USER, ],
                  message='',
                  html_message=html_message)
        messages.success(self.request, 'Ваше повідомлення успішно відправлене!')
        return super(Contact, self).form_valid(form)
