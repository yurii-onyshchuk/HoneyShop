from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class EmailPhoneNumberBackend(ModelBackend):
    """Custom authentication backend for login using email or phone number."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate a user based on their email or phone number and password."""
        try:
            user = UserModel.objects.get(Q(email__iexact=username) | Q(phone_number__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(email__iexact=username) | Q(phone_number__iexact=username)).order_by(
                'id').first()
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
