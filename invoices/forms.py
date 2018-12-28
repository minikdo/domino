from django import forms

from datetime import date

from .models import Invoice, InvoiceItem, Customer
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

    field_order = ['customer', 'number', 'issue_place', 'payment',
                   'issued', 'transaction', 'due']

    class Meta:
        model = Invoice
        fields = ['number', 'issued', 'customer', 'transaction', 'issue_place',
                  'due', 'payment']

        widgets = {'customer': forms.HiddenInput(),
                   'number': forms.TextInput(attrs={
                       'autofocus': True})}
        
        
class InvoiceItemForm(forms.ModelForm):

    make = forms.ModelChoiceField(Make.objects.all().order_by('name'),
                                  label="Nazwa towaru")

    field_order = ['make', 'price', 'qty', 'vat']
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        widgets = {'invoice': forms.HiddenInput(),
                   'vat': forms.TextInput(attrs={'size': 3}),
                   'price': forms.TextInput(attrs={'size': 5}),
                   'qty': forms.TextInput(attrs={'size': 3})}


class CustomerSearchForm(forms.Form):

    name = forms.CharField(label="nazwa",
                           widget=forms.TextInput(attrs={'autofocus': True}))
        

class CustomerForm(forms.ModelForm):

    def __init__(self, *args, session_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget = forms.TextInput(
            attrs={"autofocus": True})

    field_order = ['company',
                   'name',
                   'street',
                   'postal_code',
                   'city',
                   'tax_id',
                   'email',
                   'phone']
    
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['created_by']

