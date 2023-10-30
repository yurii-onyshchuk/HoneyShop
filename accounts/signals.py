from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

User = get_user_model()


@receiver(pre_save, sender=User)
def generate_slug(sender, instance, **kwargs):
    """Generate a slug for the user based on their phone number.

    Args:
        sender: The sender of the signal.
        instance (User): The User instance being saved.
        kwargs: Additional keyword arguments.

    This signal function is triggered before saving a User instance.
    It generates a slug for the user by slugifying their phone number and
    assigns it to the 'slug' field of the user instance.
    """

    instance.slug = slugify(instance.phone_number)
