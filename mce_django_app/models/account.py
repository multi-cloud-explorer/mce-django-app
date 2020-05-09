from itertools import chain

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django_extensions.db.fields import AutoSlugField
from rest_framework.authtoken.models import Token

from mce_django_app import constants
from mce_django_app import utils

from .common import Company, BaseModel

class User(AbstractUser):
    """MCE Account"""

    # TODO: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    role = models.CharField(
        max_length=20,
        choices=constants.UserRole.choices,
        null=True, blank=True
    )

    password = models.CharField(
                            max_length=128,
                            null=True, blank=True,
                            verbose_name=_("Password"),
                            help_text=_("Notice: No password for services accounts"))

    company = models.ForeignKey(
                            Company, 
                            null=True, blank=True,
                            on_delete=models.SET_NULL,
                            verbose_name=_("Company"))


    @property
    def is_owner(self):
        return self.role == constants.UserRole.OWNER

    @property
    def is_user(self):
        return self.role == constants.UserRole.USER

    @property
    def is_service(self):
        return self.role == constants.UserRole.SERVICE

    @property
    def api_token_key(self):
        try:
            # related_name of Token Model
            return self.auth_token.key
        except Token.DoesNotExist:
            return None

    # TODO: clean_fields: Si not role service alors password obligatoire

    def save(self, *args, **kwargs):
        """Update updated field and Call :meth:`full_clean` before saving."""
        self.full_clean()
        super().save(*args, **kwargs)

    def to_dict(self, fields=None, exclude=None):
        if not exclude:
            exclude = []
        exclude.append("auth_token")
        data = utils.model_instance_to_dict(self, fields, exclude)
        data["profile"] = self.profile.to_dict()
        return data


class UserProfile(BaseModel):

    # TODO: default lang
    # TODO: default timezone

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="profile"
    )

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
        # TODO: remplacer par un model Token avec expiration
        Token.objects.create(user=instance)

        UserProfile.objects.create(user=instance)
