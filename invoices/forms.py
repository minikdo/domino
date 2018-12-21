from django import forms

from datetime import date

from .models import Invoice, InvoiceItem
from inventory.models import Make


class InvoiceForm(forms.ModelForm):

    transaction = forms.DateField(initial=date.today(),
                                  label="Data sprzedaży",
                                  widget=forms.DateInput(format='%Y-%m-%d'),
                                  input_formats=['%Y-%m-%d'])

    issued = forms.DateField(initial=date.today(),
                             label="Data wystawienia",
                             widget=forms.DateInput(format='%Y-%m-%d'),
                             input_formats=['%Y-%m-%d'])

    due = forms.DateField(initial=date.today(),
                          label="Termin płatności",
                          widget=forms.DateInput(format='%Y-%m-%d'),
                          input_formats=['%Y-%m-%d'])

    field_order = ['customer', 'number', 'issued', 'transaction', 'due',
                   'issue_place', 'payment']

    class Meta:
        model = Invoice
        fields = ['number', 'issued', 'customer', 'transaction', 'issue_place',
                  'due', 'payment']

        widgets = {'customer': forms.HiddenInput()}
        
        
class InvoiceItemForm(forms.ModelForm):

    make = forms.ModelChoiceField(Make.objects.all(), label="Nazwa towaru")
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        widgets = {'invoice': forms.HiddenInput(),
                   'vat': forms.TextInput(attrs={'size': 3}),
                   'price': forms.TextInput(attrs={'size': 5}),
                   'qty': forms.TextInput(attrs={'size': 3})}


class CustomerSearchForm(forms.Form):

    name = forms.CharField(label="nazwa")
        
