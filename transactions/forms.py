from django import forms

from .models import CounterpartyAccount


class CounterpartyAccountCreateForm(forms.ModelForm):

    class Meta:
        model = CounterpartyAccount
        fields = ['account', 'comment', 'counterparty']
        widgets = {'counterparty': forms.HiddenInput()}
