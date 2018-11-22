from django.db.models import Sum, Q, Count, Value, F
from django.db.models.functions import Coalesce
from .models import Item, Unit


def shelf_counter(inventory, created_by, shelf_id):
    
    if any(var is None for var in [inventory, created_by, shelf_id]):
        return 0
    
    item_num = Item.objects.filter(
        Q(inventory_id=inventory),
        Q(created_by=created_by),
        Q(pk__gte=shelf_id)).aggregate(
            piece=Coalesce(
                Sum('quantity', filter=Q(unit_id=Unit.QTY_ID)), Value(0)),
            weight=Count('pk', filter=Q(unit_id=Unit.GRAM_ID)))

    return item_num


def stats(inventory):

    qty = Item.objects.filter(inventory_id=inventory, unit_id=Unit.QTY_ID)\
                      .aggregate(sum=Sum(F('price') * F('quantity')))

    gramms = Item.objects.filter(inventory_id=inventory, unit_id=Unit.GRAM_ID)\
                         .aggregate(sum=Sum('price'))
    
    return qty['sum'] + gramms['sum']


def get_total_items(inventory):
    """ multiply qty * price if qty in pieces,
    rewrite price if qty in gramms """

    items = Item.objects.filter(inventory=inventory)\
                        .values('make__name_print', 'price', 'unit__name')\
                        .annotate(
                            qty=Coalesce(
                                Sum('quantity', filter=Q(unit=1)),
                                'quantity'),
                            total=(
                                Coalesce(
                                    Sum('quantity',
                                        filter=Q(unit=1)),
                                    1) * F('price')))\
                        .prefetch_related('make', 'unit')\
                        .order_by('make__name_print', 'total')

    return items
