from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    """ shop list """

    address = models.TextField(verbose_name="sklep")

    class Meta:
        verbose_name = "adres sklepu"
        verbose_name_plural = "adresy sklepów"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse_lazy('inventory:index')


class Make(models.Model):
    """ product names """

    name = models.CharField(max_length=70, verbose_name="nazwa towaru")
    name_print = models.CharField(max_length=70,
                                  verbose_name="nazwa do druku",
                                  null=True)
    group = models.ForeignKey('MakeGroup', verbose_name="grupa towarowa",
                              on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False,
                                    verbose_name="ukryte")

    class Meta:
        verbose_name = "nazwa towaru"
        verbose_name_plural = "nazwy towarów"

    def __str__(self):
        return f"{self.id}, {self.name} {"UKRYTE" if self.is_hidden else ""}"


class MakeGroup(models.Model):
    """ make groups """

    SILVER_ID = 1
    CRAFT_ID = 2
    LINGERIE_ID = 3
    GOLD_ID = 4

    name = models.CharField(max_length=70,
                            verbose_name="nazwa grupy towarowej")

    class Meta:
        verbose_name = "grupa towarowa"
        verbose_name_plural = "grupy towarowe"

    def __str__(self):
        return self.name


class Unit(models.Model):
    """ units """

    QTY_ID = 1
    GRAM_ID = 2

    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = "jednostka miary"
        verbose_name_plural = "jednostki miar"

    def __str__(self):
        return self.name


class Item(models.Model):
    """ item list """

    MAX_PRICE = 35000
    MAX_QTY = 100

    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE,
                                  verbose_name="remanent", null=True)
    make = models.ForeignKey('Make', on_delete=models.CASCADE,
                             verbose_name="nazwa towaru")
    price = models.FloatField(verbose_name="cena brutto",
                              validators=(MinValueValidator(0.1),
                                          MaxValueValidator(MAX_PRICE)))
    quantity = models.FloatField(verbose_name="ilość",
                                 validators=(MinValueValidator(0.01),
                                             MaxValueValidator(MAX_QTY)))
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE,
                             verbose_name="j.m.")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    net_price = models.FloatField(verbose_name="cena netto", default=0,
                                  validators=(MinValueValidator(0.1),
                                              MaxValueValidator(MAX_PRICE)))

    class Meta:
        verbose_name = "remanent"
        verbose_name_plural = "remanenty"

    @property
    def price_relation(self):
        if self.net_price != 0:
            if self.unit.pk == Unit.GRAM_ID:
                return round((self.price/(self.net_price*self.quantity)), 1)
            else:
                return round((self.price/self.net_price), 1)
        else:
            return ''

    def __str__(self):
        string = "#{}, {}, cena brutto: {} zł".format(
            str(self.pk), self.make.name, str(self.price))
        return string

    def get_absolute_url(self):
        return reverse_lazy('inventory:index')

    def clean(self):
        if not isinstance(self.quantity, float):
            raise ValidationError({'quantity':
                                   'ilość powinna być liczbą (float)'})
        # Quantity cannot be fractions
        if self.unit.pk == Unit.QTY_ID and self.quantity is not None and\
           not self.quantity.is_integer():
            raise ValidationError({'quantity':
                                   _('Ilość sztuk nie może być ułamkowa')})
        # No gramms in groups other than silver and gold
        if self.unit.pk == Unit.GRAM_ID and\
           self.make.group_id not in [MakeGroup.SILVER_ID, MakeGroup.GOLD_ID]:
            raise ValidationError({'unit':
                                   _('W tej grupie towarowej nie można '
                                     'stosować gramów')})
        # Net price is higher than gross
        if self.unit.pk == Unit.QTY_ID and\
           self.net_price != 0 and\
           isinstance(self.net_price, (int, float)) and\
           isinstance(self.price, (int, float)):
            if self.net_price > self.price:
                raise ValidationError({'net_price':
                                       _('Cena netto jest wyższa niż brutto')})


class Inventory(models.Model):
    """ inventory list """

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE,
                             verbose_name="sklep")
    is_active = models.BooleanField(default=True, verbose_name="aktywny")
    net_prices = models.BooleanField(default=False,
                                     verbose_name="w cenach netto")

    class Meta:
        verbose_name = "lista remanentów"
        verbose_name_plural = "lista remanentów"

    @property
    def price_mode(self):
        """ net or gross prices """
        if self.net_prices:
            return "netto"
        else:
            return "brutto"

    def __str__(self):
        string = "{}, {}, {}, utworzył: {}, ceny: {}".format(
            str(self.pk), self.created.strftime('%Y-%m-%d'),
            self.shop.address, self.created_by.username,
            self.price_mode)
        return string

    def get_absolute_url(self):
        return reverse_lazy('inventory:inventory_select')

    def _creation_date(self):
        string = self.created.strftime('%Y-%m-%d')
        return string
