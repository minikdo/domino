from django.db.models import Sum, Q, Count, Value
from django.db.models.functions import Coalesce
from .models import Item


def shelf_counter(inventory, created_by, shelf_id):
    
    if any(var is None for var in [inventory, created_by, shelf_id]):
        return 0
    
    item_num = Item.objects.filter(
        Q(inventory_id=inventory),
        Q(created_by=created_by),
        Q(pk__gte=shelf_id)).aggregate(
            piece=Coalesce(Sum('quantity', filter=Q(unit_id=1)), Value(0)),
            weight=Count('pk', filter=Q(unit_id=2)))

    return item_num
