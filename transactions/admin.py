from django.contrib import admin

from .models import OrderingAccount, TransactionStatus

admin.site.register(OrderingAccount)
admin.site.register(TransactionStatus)
