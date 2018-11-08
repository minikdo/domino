from django.contrib import admin
from .models import Shop, Make, MakeGroup, Inventory, Item

# Register your models here.
admin.site.register(Shop)
admin.site.register(Make)
admin.site.register(MakeGroup)
admin.site.register(Inventory)
admin.site.register(Item)
