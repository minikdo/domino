from django.db.models import Sum, F, FloatField

from .models import InvoiceItem


def SumItems(invoice):
    items = InvoiceItem.objects.filter(invoice=invoice)

    # calculate tax amount
    sum = items.aggregate(
        sum=Sum(F('price') * F('qty'),
                output_field=FloatField()),
        net_sum=Sum(
            (F('price')/(1+(F('vat')/100)) * F('qty')),
            output_field=FloatField()))

    # group prices by vat tax
    sum2 = items.values('vat').annotate(
        sum_vat=Sum(
            (F('price')-(F('price')/(1+(F('vat')/100))))*F('qty'),
            output_field=FloatField()
        ))

    return sum, sum2
