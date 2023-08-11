from django.conf import settings
from django.core.files.base import ContentFile
from django.urls import reverse
from django.contrib.auth import get_user_model

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from urllib.request import urlopen

user_model = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:  # Already linked
            return
        try:  # if user exists, connect the account to the existing account and login
            UserObj = user_model.objects.get(email=user.email)
            sociallogin.state['process'] = 'connect'
            perform_login(request, UserObj, 'none')
        except user_model.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):
        self.populate_user_avatar(sociallogin)
        return super().save_user(request, sociallogin, form)

    @staticmethod
    def populate_user_avatar(sociallogin):
        picture_url = sociallogin.account.get_avatar_url()
        user = sociallogin.user
        picture = ContentFile(urlopen(picture_url).read())
        user.photo.save(f'{user.first_name}_{user.last_name}.jpg', picture, save=False)
        urlopen(picture_url).close()

    def get_connect_redirect_url(self, request, socialaccount):
        return reverse(settings.LOGIN_REDIRECT_URL)
