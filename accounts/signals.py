from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

User = get_user_model()


@receiver(pre_save, sender=User)
def generate_slug(sender, instance, **kwargs):
    """
    Generate a slug for the user based on their username.
    """
    instance.slug = slugify(instance.phone_number)
