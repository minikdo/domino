from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Make, MakeGroup, Inventory, Unit, Item


class ItemForm(forms.ModelForm):
    """ Inventory item form """
        
    def __init__(self, *args, session_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['make'].queryset = self.fields['make'].queryset.filter(
            group=session_data['group_id']).order_by('name')

        # check if the inventory is in net prices
        net_prices = Inventory.objects.get(pk=session_data['inventory_id'])\
                                      .net_prices
        if not net_prices:
            # remove net_price field for gross only inventories
            self.fields.pop('net_price')
            self.fields['price'].widget = forms.TextInput(attrs={
                'autofocus': True})
            
    make = forms.ModelChoiceField(Make.objects.all(),
                                  label="")

    net_price = forms.CharField(label="",
                                widget=forms.TextInput(
                                    attrs={'autofocus': True,
                                           'class': 'form-number',
                                           'size': 6}))
    price = forms.CharField(label="",
                            widget=forms.TextInput(
                                attrs={'size': 6,
                                       'class': 'form-number'}))
    quantity = forms.CharField(label="",
                               widget=forms.TextInput(
                                   attrs={'size': 6,
                                          'class': 'form-number'}))
    unit = forms.ModelChoiceField(Unit.objects.all(), label="")

    field_order = ['make', 'net_price', 'price', 'quantity', 'unit']

    class Meta:
        model = Item
        fields = ['make', 'net_price', 'price', 'quantity', 'unit']
    

class InventorySelectForm(forms.Form):
    """ Inventory select form """

    inventory = forms.ModelChoiceField(queryset=Inventory.objects.all(),
                                       label="remanent")
    group = forms.ModelChoiceField(queryset=MakeGroup.objects.all(),
                                   label="dział")


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, label="Imię")
    last_name = forms.CharField(max_length=32, label="Nazwisko")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')


class ItemSearchForm(forms.Form):
    """ Item search """

    # FIXME
    def __init__(self, *args, session_data=None, **kwargs):
        super().__init__(*args, **kwargs)

        make_ids = Item.objects\
                       .filter(inventory_id=session_data['inventory_id'])\
                       .values_list('make_id', flat=True)
        self.fields['make'].queryset = self.fields['make']\
                                           .queryset\
                                           .filter(id__in=set(make_ids))\
                                           .order_by('name')

        # check if the inventory is in net prices
        net_prices = Inventory.objects.get(pk=session_data['inventory_id'])\
                                      .net_prices
        if not net_prices:
            self.fields['net_price'].disabled = True
        
    id = forms.IntegerField(required=False, label="id",
                            widget=forms.TextInput(attrs={
                                'size': 6,
                                'autocomplete': 'off'
                            }))
    make = forms.ModelChoiceField(
        queryset=Make.objects.exclude(item__make=None),
        label="nazwa towaru",
        required=False,
        widget=forms.Select(
            attrs={'autofocus': True}))
    net_price = forms.FloatField(label="cena netto", required=False,
                                 widget=forms.TextInput(
                                     attrs={'size': 6}))
    price = forms.FloatField(label="cena brutto", required=False,
                             widget=forms.TextInput(attrs={
                                 'size': 6
                             }))
    myuser = forms.ModelChoiceField(
        queryset=User.objects.exclude(item__created_by=None),
        label="osoba",
        required=False)
    show_all = forms.BooleanField(label="wszystko", required=False)
