from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    """ shop list """
    
    address = models.TextField(verbose_name="sklep")

    def __str__(self):
        return self.address
    
    def get_absolute_url(self):
        return reverse_lazy('index')


class Make(models.Model):
    """ product names """
    
    name = models.CharField(max_length=70, verbose_name="nazwa towaru")
    name_print = models.CharField(max_length=70,
                                  verbose_name="nazwa do druku",
                                  null=True)
    group = models.ForeignKey('MakeGroup', verbose_name="grupa towarowa",
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MakeGroup(models.Model):
    """ make groups """

    name = models.CharField(max_length=70,
                            verbose_name="nazwa grupy towarowej")

    def __str__(self):
        return self.name


class Unit(models.Model):
    """ units """

    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class Item(models.Model):
    """ item list """
    
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE,
                                  verbose_name="remanent", null=True)
    make = models.ForeignKey('Make', on_delete=models.CASCADE,
                             verbose_name="nazwa towaru")
    price = models.FloatField(verbose_name="cena brutto")
    quantity = models.FloatField(verbose_name="ilość")
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE,
                             verbose_name="j.m.")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        string = '#' + str(self.pk) + ', ' + self.make.name
        string += ', cena: ' + str(self.price) + ' zł'
        return string
    
    def get_absolute_url(self):
        return reverse_lazy('index')

    def clean(self):
        if self.price <= 0:
            raise ValidationError({'price':
                                   _('Cena nie może wynosić 0 lub mniej')})
        if self.quantity <= 0 or self.quantity > 100:
            raise ValidationError({'quantity':
                                   _('Ilość musi być większa od 0 i mniejsza '
                                     'od 100')})
        if self.unit.pk == 1 and int(self.quantity) != self.quantity:
            raise ValidationError({'quantity':
                                   _('Ilość sztuk nie może być ułamkowa')})
        if self.unit.pk == 2 and self.make.group_id != 4:
            raise ValidationError({'unit':
                                   _('W tej grupie towarowej nie można '
                                     'stosować gramów')})


class Inventory(models.Model):
    """ inventory list """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE,
                             verbose_name="sklep")
    active = models.BooleanField(default=True)

    def __str__(self):
        string = str(self.pk) + ', '
        string += self.created.strftime('%Y-%m-%d') + ', ' + self.shop.address
        string += ', utworzył: ' + self.created_by.username
        return string

    class Meta:
        verbose_name = "remanent"
        verbose_name_plural = "remanenty"

    def get_absolute_url(self):
        return reverse_lazy('inventory_select')
