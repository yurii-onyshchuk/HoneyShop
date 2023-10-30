from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import ContactForm


class Home(TemplateView):
    """View for home page."""

    extra_context = {'title': 'Головна'}
    template_name = 'main/index.html'


class About(TemplateView):
    """View for page with information about us."""

    extra_context = {'title': 'Про нас'}
    template_name = 'main/about.html'


class Contact(FormView):
    """View for page with a contact form."""

    extra_context = {'title': 'Контакти'}
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def get_initial(self):
        """Return the name and email of the authenticated user as default values in the contact form."""
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.first_name
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        """If the form is valid, send a message from the contact form and redirect to the supplied URL."""
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
