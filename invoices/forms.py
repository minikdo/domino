from django import forms

from datetime import date

from .models import Invoice, InvoiceItem
from inventory.models import Make


class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, session_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True

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

    class Meta:
        model = Invoice
        fields = ['number', 'issued', 'customer', 'transaction',
                  'due']


class InvoiceItemForm(forms.ModelForm):

    make = forms.ModelChoiceField(Make.objects.all())
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
