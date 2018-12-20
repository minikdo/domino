from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from transactions.validators import validate_tax_id
from transactions.models import TimeStampedModel
from inventory.models import Make


class Invoice(TimeStampedModel):
    """ invoices """

    number = models.CharField(max_length=35, verbose_name="numer faktury")
    customer = models.ForeignKey('Customer',
                                 verbose_name="klient",
                                 on_delete=models.CASCADE)
    issued = models.DateField(verbose_name="data wystawienia")
    transaction = models.DateField(verbose_name="data sprzedaży")
    due = models.DateField(verbose_name="termin płatności")
    
    def __str__(self):
        string = "{}, {}, {}".format(
            self.number, self.issued, self.customer)
        return string

    def get_absolute_url(self):
        return reverse('invoices:detail',
                       kwargs={'pk': self.id})


class InvoiceItem(models.Model):
    """ items on invoice """

    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    make = models.ForeignKey(Make, verbose_name="towar",
                             on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                verbose_name="cena brutto")
    vat = models.FloatField(default=23, help_text="%")
    qty = models.FloatField(default=1, verbose_name="ilość")

    @property
    def net_price(self):
        """ calculate net price """
        
        return round(float(self.price)/(1+(self.vat/100)), 2)

    def __str__(self):
        string = "{}, {}, {}, {}".format(
            self.make, self.qty, self.price, self.vat)
        return string

    def get_absolute_url(self):
        return reverse('invoices:detail',
                       kwargs={'pk': self.invoice.pk})


class Customer(TimeStampedModel):
    """ counterparties """

    company = models.CharField(max_length=35,
                               null=True,
                               blank=True,
                               verbose_name="nazwa firmy")
    name = models.CharField(max_length=35,
                            null=True,
                            blank=True,
                            verbose_name="imię i nazwisko")
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
                              help_text="tylko cyfry")
    email = models.EmailField(max_length=50,
                              blank=True,
                              null=True)
    phone = models.CharField(max_length=35,
                             blank=True,
                             null=True,
                             verbose_name="telefon")

    class Meta:
        verbose_name = "klient"
        verbose_name_plural = "klienci"

    def __str__(self):
        string = "{}, {}, {}, {}, {}".format(
            self.company,
            self.name,
            self.street,
            self.city,
            self.tax_id)
        return string

    def get_absolute_url(self):
        return reverse('invoices:customer-detail',
                       kwargs={'pk': self.id})

    def clean(self):
        if self.tax_id is not None and\
           self.tax_id.isdigit() and\
           not validate_tax_id(self.tax_id):
            raise ValidationError({'tax_id':
                                   _('Nieprawidłowa suma kontrolna NIP')})
