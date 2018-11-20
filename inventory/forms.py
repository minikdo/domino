from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from collections import OrderedDict
from .models import Make, MakeGroup, Inventory, Unit


class ItemForm(forms.Form):
    """ Inventory item form """

    def __init__(self, *args, session_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['make'] = forms.ModelChoiceField(
            Make.objects.filter(group=session_data['group_id'])
            .order_by('name'),
            empty_label=None, label="")
        keys = ['make', 'price', 'quantity', 'unit']
        self.fields = OrderedDict(sorted(self.fields.items(),
                                         key=lambda x: keys.index(x[0])))

    price = forms.CharField(label="",
                            widget=forms.TextInput(
                                attrs={'autofocus': True,
                                       'size': 10}))
    quantity = forms.CharField(label="",
                               widget=forms.TextInput(
                                   attrs={'size': 10}))
    unit = forms.ModelChoiceField(Unit.objects.all(), label="")
    

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

    make = forms.ModelChoiceField(queryset=Make.objects.all(),
                                  label="nazwa towaru",
                                  required=False,
                                  widget=forms.Select(
                                      attrs={'autofocus': True}))
    price = forms.FloatField(label="cena brutto", required=False,
                             widget=forms.TextInput(attrs={
                                 'size': 6
                             }))
    myuser = forms.ModelChoiceField(queryset=User.objects.exclude(item__created_by=None),
                                  label="osoba",
                                  required=False)
    show_all = forms.BooleanField(label="wszystko", required=False)
