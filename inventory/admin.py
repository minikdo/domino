from django.contrib import admin
from .models import Shop, Make, MakeGroup, Inventory, Item


@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'is_hidden']

# Register your models here.
admin.site.register(Shop)
admin.site.register(MakeGroup)
admin.site.register(Inventory)
admin.site.register(Item)
