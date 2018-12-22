from django import forms
# from django.urls import reverse_lazy, reverse

# from dal.autocomplete import ListSelect2

from datetime import date

from .models import Counterparty, CounterpartyAccount, Transaction


class TransactionForm(forms.ModelForm):

    def __init__(self, *args, session_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['counterparty_account'].disabled = True
        self.fields['counterparty_account'].label = "Rachunek odbiorcy"
        self.fields['ordering_account'].label = "Rachunek obciążany"

    execution_date = forms.DateField(initial=date.today(),
                                     label="Data wykonania",
                                     widget=forms.DateInput(format='%Y-%m-%d'),
                                     input_formats=['%Y-%m-%d'])

    order_title = forms.CharField(label="Tytuł przelewu",
                                  widget=forms.Textarea(
                                      attrs={'cols': 35,
                                             'rows': 4,
                                             'maxlength': 140}))

    field_order = ['ordering_account', 'counterparty_account', 'amount',
                   'order_title', 'execution_date']
    
    class Meta:
        model = Transaction
        
        fields = ['execution_date',
                  'amount',
                  'order_title',
                  'counterparty_account',
                  'ordering_account',
                  'transaction_type',
                  'transaction_classification']

        widgets = {'transaction_type': forms.HiddenInput(),
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
