from django import forms

from datetime import date


class ContractForm(forms.Form):

    date = forms.DateField(initial=date.today(),
                           label="Data sprzedaży",
                           widget=forms.DateInput(format='%Y-%m-%d'),
                           input_formats=['%Y-%m-%d'])
    
    number = forms.CharField(label="Numer umowy",
                             widget=forms.TextInput(
                                 attrs={'autofocus': True}))

    seller = forms.CharField(label="Sprzedający")
    weight = forms.FloatField(label="Waga")
    price = forms.FloatField(label="Cena")
