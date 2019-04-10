from django.db import models
from django.urls import reverse


class Machine(models.Model):
    name = models.CharField(max_length=50)
    FQDN = models.CharField(max_length=50, null=True, blank=True)
    datetime = models.DateField(null=True, blank=True)
    form = models.CharField(max_length=50, null=True, blank=True)
    bios = models.CharField(max_length=50, null=True, blank=True)
    prod = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.CharField(max_length=50, null=True, blank=True)
    OS = models.CharField(max_length=50, null=True, blank=True)
    kernel = models.CharField(max_length=50, null=True, blank=True)
    CPU = models.CharField(max_length=50, null=True, blank=True)
    cores = models.CharField(max_length=50, null=True, blank=True)
    arch = models.CharField(max_length=50, null=True, blank=True)
    mem = models.CharField(max_length=50, null=True, blank=True)
    HDD = models.CharField(max_length=50, null=True, blank=True)
    disk = models.CharField(max_length=50, null=True, blank=True)
    diskfree = models.CharField(max_length=50, null=True, blank=True)
    IPs = models.CharField(max_length=50, null=True, blank=True)
    gateway = models.CharField(max_length=50, null=True, blank=True)
    gate_iface = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    # device = models.ManyToManyField('Device')
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('machines:index')


class Service(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=300)
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
                                on_delete=models.SET_NULL)
    date = models.DateField(null=True, blank=True)
    type = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    price = models.DecimalField(max_digits=5,
                                decimal_places=0,
                                blank=True,
                                null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    invoice = models.CharField(max_length=150, blank=True, null=True)
    location = models.ForeignKey('Location', null=True, blank=True,
                                 on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('machines:device_index')

    def __str__(self):
        string = "{} {}".format(str(self.date), self.name)
        return string


class DeviceType(models.Model):
    name = models.CharField(unique=True, max_length=150, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
    

class Location(models.Model):
    """ machine location list """

    address = models.CharField(max_length=150)

    def __str__(self):
        return self.address
