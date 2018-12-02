from django.db import models
from django.contrib.auth.models import User


class TransactionStatus(models.Model):
    """ transaction status """

    name = models.CharField(max_length=30, verbose_name="status")

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "statusy"

    def __str__(self):
        return self.name


class Transaction(models.Model):
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
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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


class TransactionFile(models.Model):
    """ transaction package """

    pass


class Counterparty(models.Model):
    """ counterparties """

    account = models.ForeignKey('Account',
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name="konto")
    name = models.CharField(max_length=35, null=True, verbose_name="nazwa")
    street = models.CharField(max_length=35, null=True, verbose_name="ulica")
    city = models.CharField(max_length=35, null=True, verbose_name="miasto")
    tax_id = models.CharField(max_length=35, null=True, verbose_name="NIP")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "kontrahent"
        verbose_name_plural = "kontrahenci"

    def __str__(self):
        string = "{}, {}, {}, {}".format(
            self.name,
            self.street,
            self.city,
            self.nip)
        return string


class Account(models.Model):
    """ account numbers """
    """ one counterparty may have many bank accounts """

    account = models.CharField(max_length=34, verbose_name="numer konta")
    comment = models.CharField(max_length=50, verbose_name="komentarz")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "konto bankowe"
        verbose_name_plural = "konta bankowe"

    def __str__(self):
        return self.account
