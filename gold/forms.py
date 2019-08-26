from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

from datetime import date


class ContractForm(forms.Form):

    date = forms.DateField(widget=widgets.AdminDateWidget(),
                           localize=False,
                           initial=date.today(),
                           input_formats=['%d.%m.%Y'])

    number = forms.CharField(label="Numer umowy",
                             widget=forms.TextInput(
                                 attrs={'autofocus': True}))

    seller = forms.CharField(label="Umowa zawarta z")
    weight = forms.FloatField(label="Waga")
    price = forms.FloatField(label="Cena")

    class Media:
        js = ('admin/js/vendor/jquery/jquery.js',
              'admin/js/core.js')
        css = {'all': ('admin/css/forms.css',)}

    def clean_seller(self):
        seller = self.cleaned_data['seller']
        if len(seller) > 50:
            raise ValidationError("Nazwa przekracza 50 znaków")
        return seller
