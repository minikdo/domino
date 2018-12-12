from django import forms
# from django.urls import reverse_lazy, reverse

# from dal.autocomplete import ListSelect2

from .models import Counterparty, CounterpartyAccount, Transaction


class TransactionFrom(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['execution_date', 'amount', 'order_title']


class CounterpartyAccountCreateForm(forms.ModelForm):

    class Meta:
        model = CounterpartyAccount
        fields = ['account', 'comment', 'counterparty']
        widgets = {'counterparty': forms.HiddenInput()}

        
class CounterpartySearch(forms.ModelForm):

    name = forms.CharField(required=False,
                           widget=forms.TextInput(
                               attrs={'autofocus': True}))
    
    class Meta:
        model = Counterparty
        fields = ['name', 'tax_id']
        # widgets = {'name': ListSelect2(
            # url='transactions:counterparty-autocomplete',
            # attrs={'class': 'form-control'})
        # }
