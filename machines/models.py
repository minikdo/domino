from django.db import models
from django.urls import reverse


class Machine(models.Model):
    name = models.CharField(max_length=50)
    FQDN = models.CharField(max_length=50, null=True)
    datetime = models.DateField()
    form = models.CharField(max_length=50, null=True)
    bios = models.CharField(max_length=50, null=True)
    prod = models.CharField(max_length=50, null=True)
    vendor = models.CharField(max_length=50, null=True)
    OS = models.CharField(max_length=50, null=True)
    kernel = models.CharField(max_length=50, null=True)
    CPU = models.CharField(max_length=50, null=True)
    cores = models.CharField(max_length=50, null=True)
    arch = models.CharField(max_length=50, null=True)
    mem = models.CharField(max_length=50, null=True)
    HDD = models.CharField(max_length=50, null=True)
    disk = models.CharField(max_length=50, null=True)
    diskfree = models.CharField(max_length=50, null=True)
    IPs = models.CharField(max_length=50, null=True)
    gateway = models.CharField(max_length=50, null=True)
    gate_iface = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.FQDN


class Service(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=300)
    device = models.ForeignKey('Device',
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.machine_id})

    def __str__(self):
        return self.description


class Device(models.Model):
    komp = models.ForeignKey('Machine',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    date = models.DateField()
    type = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    price = models.DecimalField(max_digits=5,
                                decimal_places=0,
                                blank=True,
                                null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    invoice = models.CharField(max_length=150, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('device_index')

    def __str__(self):
        string = "{} {}".format(str(self.date), self.name)
        return string


class DeviceType(models.Model):
    name = models.CharField(unique=True, max_length=150, null=True)

    def __str__(self):
        return self.name
