from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token
from .common import Company

class User(AbstractUser):
    """MCE Account"""

    password = models.CharField(
                            max_length=128,
                            null=True,
                            verbose_name=_("Mot de passe"), 
                            help_text=_("Remarque: Les comptes de service n'ont pas de mot de passe"))

    company = models.ForeignKey(
                            Company, 
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name=_("Société"))


    is_service = models.BooleanField(
                            default=False,
                            verbose_name=_("Compte de service ?"))


    @property
    def api_token_key(self):
        try:
            # related_name of Token Model
            return self.auth_token.key
        except Token.DoesNotExist:
            return None

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create token for newly created user.
    """
    if created:
        Token.objects.create(user=instance)

