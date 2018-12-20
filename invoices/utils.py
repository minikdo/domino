from django.db.models import Sum, F, FloatField

from .models import InvoiceItem


def SumItems(invoice):
    items = InvoiceItem.objects.filter(invoice=invoice)
    sum = items.aggregate(sum=Sum(F('price') * F('qty'),
                                  output_field=FloatField()))
    return sum
