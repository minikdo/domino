from django import forms
# from django.urls import reverse_lazy, reverse

# from dal.autocomplete import ListSelect2

from datetime import date

from .models import Counterparty, CounterpartyAccount, Transaction,\
    OrderingAccount


class TransactionForm(forms.ModelForm):
    
    ordering_account = forms.ModelChoiceField(OrderingAccount.objects.all(),
                                              to_field_name='account',
                                              label="Wybierz konto")
    
    execution_date = forms.DateField(initial=date.today(),
                                     label="Data wykonania",
                                     widget=forms.DateInput(format='%Y-%m-%d'),
                                     input_formats=['%Y-%m-%d'])

    order_title = forms.CharField(
        label="Tytuł przelewu",
        widget=forms.Textarea(
            attrs={'cols': 35,
                   'rows': 3,
                   'maxlength': 150}))
    
    class Meta:
        model = Transaction
        
        fields = ['execution_date',
                  'amount',
                  'order_title',
                  'counterparty_account',
                  'ordering_account',
                  'transaction_type',
                  'transaction_classification']

        widgets = {'counterparty_account': forms.HiddenInput(),
                   'transaction_type': forms.HiddenInput(),
                   'transaction_classification': forms.HiddenInput()}


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
