from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField
from rest_framework.authtoken.models import Token

from .common import Company, BaseModel

class User(AbstractUser):
    """MCE Account"""

    # TODO: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    is_service = models.BooleanField(
                            default=False,
                            verbose_name=_("Service Account ?"))

    password = models.CharField(
                            max_length=128,
                            null=True,
                            verbose_name=_("Password"),
                            help_text=_("Notice: No password for services accounts"))

    company = models.ForeignKey(
                            Company, 
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name=_("Company"))


    @property
    def api_token_key(self):
        try:
            # related_name of Token Model
            return self.auth_token.key
        except Token.DoesNotExist:
            return None

class UserProfile(BaseModel):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)

    slug = AutoSlugField(
        primary_key=True,
        max_length=300,
        populate_from=['user__username'],
        overwrite=True,
        unique=True
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create token for newly created user.
    """
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
        # assign_perm("change_user", user, user)
        # assign_perm("change_profile", user, profile)

