from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator,\
    MaxLengthValidator, int_list_validator
from django.utils.translation import gettext_lazy as _

from .validators import validate_nip, validate_iban


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified``
    and ``created_by`` fields.
    """
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        abstract = True


class TransactionStatus(TimeStampedModel):
    """ transaction status """

    name = models.CharField(max_length=30, verbose_name="status")

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "statusy"

    def __str__(self):
        return self.name


class Transaction(TimeStampedModel):
    """ transactions """
    """ format EXILIR-0 """
    
    transaction_type = models.IntegerField()
    execution_date = models.IntegerField()
    amount = models.IntegerField()
    ordering_bank = models.IntegerField()
    ordering_account = models.CharField(max_length=34)
    counterparty_account = models.CharField(max_length=34)
    ordering_name_address = models.CharField(max_length=150)
    counterparty_name_address = models.CharField(max_length=150)
    counterparty_bank = models.IntegerField()
    order_title = models.CharField(max_length=150)
    transaction_classification = models.IntegerField()
    annotations = models.CharField(max_length=32)
    # additional fields:
    status = models.ForeignKey('TransactionStatus',
                               null=True,
                               on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "transakcja"
        verbose_name_plural = "transakcje"

    def __str__(self):
        string = "{}, {}, {}".format(
            self.execution_date,
            self.counterparty_account,
            self.amount)
        return string


class TransactionFile(TimeStampedModel):
    """ transaction package """

    transaction = models.ManyToManyField('Transaction')

    class Meta:
        verbose_name = "paczka przelewów"
        verbose_name_plural = "paczki przelewów"

    def __str__(self):
        return self.transaction
    

class Counterparty(TimeStampedModel):
    """ counterparties """

    name = models.CharField(max_length=35,
                            null=True,
                            verbose_name="nazwa")
    street = models.CharField(max_length=35,
                              null=True,
                              blank=True,
                              verbose_name="ulica")
    city = models.CharField(max_length=35,
                            blank=True,
                            null=True,
                            verbose_name="miasto")
    tax_id = models.CharField(max_length=35,
                              blank=True,
                              null=True,
                              unique=True,
                              verbose_name="NIP",
                              help_text="NIP: same cyfry bez kresek")

    class Meta:
        verbose_name = "kontrahent"
        verbose_name_plural = "kontrahenci"

    def __str__(self):
        string = "{}, {}, {}, {}".format(
            self.name,
            self.street,
            self.city,
            self.tax_id)
        return string

    def get_absolute_url(self):
        return reverse('transactions:counterparty-detail',
                       kwargs={'pk': self.id})

    def clean(self):
        if not validate_nip(self.tax_id):
            raise ValidationError({'tax_id':
                                   _('Nieprawidłowy NIP')})


class CounterpartyAccount(TimeStampedModel):
    """ account numbers """
    """ one counterparty may have many bank accounts """

    account = models.CharField(validators=[
        MinLengthValidator(26),
        MaxLengthValidator(26),
        int_list_validator(sep='')],  # FIXME: slow cpu
                               max_length=26,
                               unique=True,
                               verbose_name="numer konta")
    comment = models.CharField(max_length=50,
                               blank=True,
                               verbose_name="komentarz")
    counterparty = models.ForeignKey('Counterparty',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     verbose_name="kontrahent")

    class Meta:
        verbose_name = "konto bankowe"
        verbose_name_plural = "konta bankowe"

    def __str__(self):
        return self.account

    def get_absolute_url(self):
        return reverse('transactions:counterparty-detail',
                       kwargs={'pk': self.counterparty_id})

    def clean(self):
        if not validate_iban(self.account):
            raise ValidationError({'account':
                                   _('Nieprawidłowy numer konta')})
