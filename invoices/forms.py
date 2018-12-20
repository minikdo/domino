from django import forms

from .models import Invoice


class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, session_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True

    class Meta:
        model = Invoice
        fields = ['number', 'issued', 'customer', 'transaction',
                  'due']        
