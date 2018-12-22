from django.contrib import admin

from .models import Counterparty, OrderingAccount, TransactionStatus

admin.site.register(OrderingAccount)
admin.site.register(TransactionStatus)
admin.site.register(Counterparty)
