from django.contrib import admin

from .models import Invoice, InvoiceItem, Customer


admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Customer)
