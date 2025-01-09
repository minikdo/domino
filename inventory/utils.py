from django.db.models import Sum, Q, Count, Value, F, IntegerField
from django.db.models.functions import Coalesce
from .models import Item, Unit, Inventory


def shelf_counter(inventory, created_by, shelf_id):

    if any(var is None for var in [inventory, created_by, shelf_id]):
        return 0

    item_num = Item.objects.filter(
        Q(inventory_id=inventory),
        Q(created_by=created_by),
        Q(pk__gte=shelf_id)).aggregate(
            piece=Coalesce(
                Sum('quantity', filter=Q(unit_id=Unit.QTY_ID),
                    output_field=IntegerField()), Value(0)),
            weight=Count('pk', filter=Q(unit_id=Unit.GRAM_ID)))

    return item_num


def stats(inventory):

    items = Item.objects.filter(inventory_id=inventory)

    qty = items.filter(unit_id=Unit.QTY_ID)
    gramms = items.filter(unit_id=Unit.GRAM_ID)

    gramms_net = gramms.aggregate(
        sum=Sum(F('net_price') * F('quantity')))['sum'] or 0.00
    qty_net = qty.aggregate(
        sum=Sum(F('net_price') * F('quantity')))['sum'] or 0.00

    qty_gross = qty.aggregate(
        sum=Sum(F('price') * F('quantity')))['sum'] or 0.00
    gramms_gross = gramms.aggregate(
        sum=Sum(F('price')))['sum'] or 0.00

    return {
        "net": qty_net + gramms_net,
        "gross": qty_gross + gramms_gross,
    }


def get_total_items(inventory):
    """ multiply qty * price if qty in pieces,
    rewrite price if qty in gramms """

    net_prices = Inventory.objects.get(pk=inventory).net_prices

    if net_prices:
        price = 'net_price'
    else:
        price = 'price'

    items = Item.objects.filter(inventory=inventory)\
                        .values('make__name_print', price, 'unit__name')

    if net_prices:
        items = items.annotate(
            qty=Sum('quantity'),
            total=(Sum('quantity') * F(price)))
    else:
        items = items.annotate(
            qty=Coalesce(
                Sum('quantity', filter=Q(unit=Unit.QTY_ID)),
                'quantity'),
            total=(
                Coalesce(
                    Sum('quantity',
                        filter=Q(unit=Unit.QTY_ID),
                        output_field=IntegerField()),
                    1) * F(price)))

    items = items.prefetch_related('make', 'unit')\
                 .order_by('make__name_print', price)

    return items


def sum_by_group(items):
    # bielizna, wyr. art.
    sums = items\
        .filter(make__group__in=[2, 3])\
        .values('make__group__name')\
        .annotate(sum=Sum(F('price') * F('quantity')))

    return sums
