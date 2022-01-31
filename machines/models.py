from django.db import models
from django.urls import reverse

from datetime import date as datetime_date
import os
from uuid import uuid4


def device_upload_location(instance, filename):
    fname, ext = os.path.splitext(filename)
    name = instance.pk if instance.pk else uuid4().hex
    return "device/{name}{ext}".format(name=name, ext=ext)


class Machine(models.Model):
    name = models.CharField(max_length=50)
    FQDN = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    form = models.CharField(max_length=50, null=True, blank=True)
    bios = models.CharField(max_length=50, null=True, blank=True)
    prod = models.CharField(max_length=150, null=True, blank=True)
    vendor = models.CharField(max_length=150, null=True, blank=True)
    OS = models.CharField(max_length=150, null=True, blank=True)
    kernel = models.CharField(max_length=150, null=True, blank=True)
    CPU = models.CharField(max_length=150, null=True, blank=True)
    cores = models.CharField(max_length=150, null=True, blank=True)
    arch = models.CharField(max_length=150, null=True, blank=True)
    mem = models.CharField(max_length=250, null=True, blank=True)
    HDD = models.CharField(max_length=250, null=True, blank=True)
    disk = models.CharField(max_length=250, null=True, blank=True)
    diskfree = models.CharField(max_length=250, null=True, blank=True)
    IPs = models.CharField(max_length=350, null=True, blank=True)
    gateway = models.CharField(max_length=250, null=True, blank=True)
    gate_iface = models.CharField(max_length=250, null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('machines:detail', kwargs={'pk': self.pk})

    @property
    def outdated_setup(self):
        if not self.date:
            return False
        dt = datetime_date.today() - self.date
        if dt.days > 90:
            return True
        else:
            return False

    @property
    def days_since(self):
        if self.date is not None:
            ds = (datetime_date.today() - self.date)
            return ds.days
        return ''


class Service(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(max_length=500)
    device = models.ForeignKey('Device',
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('machines:detail', kwargs={'pk': self.machine_id})

    def __str__(self):
        return self.description


class Device(models.Model):
    machine = models.ForeignKey('Machine',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='device')
    date = models.DateField(null=True, blank=True)
    type = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    price = models.DecimalField(max_digits=5,
                                decimal_places=0,
                                blank=True,
                                null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    invoice = models.CharField(max_length=150, blank=True, null=True,
                               verbose_name='invoice number')
    location = models.ForeignKey('Location', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    serial = models.CharField(max_length=150, blank=True, null=True,
                              verbose_name='serial number')
    invoice_pdf = models.FileField(upload_to=device_upload_location,
                                   blank=True, null=True)

    def get_absolute_url(self):
        return reverse('machines:device_detail', kwargs={'pk': self.pk})

    def __str__(self):
        string = "{} {}".format(str(self.date), self.name)
        return string

    class Meta:
        ordering = ['-pk']


class DeviceType(models.Model):
    name = models.CharField(unique=True, max_length=150, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Location(models.Model):
    """ machine location list """

    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.address
