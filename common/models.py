from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator,\
    MaxLengthValidator
from django.utils.translation import gettext_lazy as _

from .validators import validate_tax_id, validate_iban


class IbanValidator(models.Model):

    def clean(self):
        if not self.account.isdigit():
            raise ValidationError({'account':
                                   _('W numerze powinny być tylko cyfry')})
        if not validate_iban(self.account):
            raise ValidationError({'account':
                                   _('Nieprawidłowy numer konta')})

    class Meta:
        abstract = True
        

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified``
    and ``created_by`` fields.
    """
    
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        abstract = True
