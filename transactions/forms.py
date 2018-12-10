from django import forms
# from django.urls import reverse_lazy, reverse

from dal.autocomplete import ListSelect2

from .models import Counterparty, CounterpartyAccount


class CounterpartyAccountCreateForm(forms.ModelForm):

    class Meta:
        model = CounterpartyAccount
        fields = ['account', 'comment', 'counterparty']
        widgets = {'counterparty': forms.HiddenInput()}


class CounterpartySearch(forms.ModelForm):

    # name = forms.ModelChoiceField(
        # queryset=Counterparty.objects.all(),
        # widget=ModelSelect2(
            # url=reverse_lazy('transactions:counterparty-autocomplete')))

    class Meta:
        model = Counterparty
        fields = ['name', 'tax_id']
        widgets = {'name': ListSelect2(
            url='transactions:counterparty-autocomplete',
            attrs={'class': 'form-control'})
        }
            
