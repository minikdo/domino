# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from dal.autocomplete import Select2QuerySetView, Select2ListView

from .models import Transaction, Counterparty, CounterpartyAccount
from .forms import CounterpartyAccountCreateForm, CounterpartySearch
from .mixins import CreatedByMixin


class IndexView(LoginRequiredMixin, ListView):
    """ transaction list """

    model = Transaction
    template_name = 'transactions/index.html'


class CounterpartyIndexView(LoginRequiredMixin, FormMixin, ListView):
    """ counterparty list """

    model = Counterparty
    ordering = ['name']
    template_name = 'transactions/counterparty_index.html'
    form_class = CounterpartySearch


class CounterpartyDetailView(LoginRequiredMixin, DetailView):
    """ counterparty details """

    model = Counterparty
    template_name = 'transactions/counterparty_detail.html'


class CounterpartyCreate(LoginRequiredMixin, CreatedByMixin, CreateView):
    """ create a counterparty """

    model = Counterparty
    fields = ['name', 'street', 'city', 'tax_id']
    template_name = 'transactions/counterparty_create.html'


class CounterpartyUpdate(LoginRequiredMixin, UpdateView):
    """ update a counterparty """
    
    model = Counterparty
    fields = ['name', 'street', 'city', 'tax_id']
    template_name = 'transactions/counterparty_update.html'


class CounterpartyDelete(LoginRequiredMixin, DeleteView):
    """ delete a counterparty """

    model = Counterparty
    template_name = 'transactions/counterparty_confirm_delete.html'
    success_url = '/'


class CounterpartyAutocomplete(LoginRequiredMixin, Select2ListView):
    
    def get_list(self):

        qs = Counterparty.objects.all()
        
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
            
        return qs.values_list('name', flat=True).order_by('name')
    

class CounterpartyAccountCreate(LoginRequiredMixin,
                                CreatedByMixin,
                                CreateView):
    """ create a counterpartys' bank account"""

    model = CounterpartyAccount
    template_name = 'transactions/bankaccount_create.html'
    form_class = CounterpartyAccountCreateForm

    def get_initial(self):
        return {'counterparty': self.counterparty}
        
    def dispatch(self, request, *args, **kwargs):
        self.counterparty = kwargs.get('counterparty')
        return super().dispatch(request, *args, **kwargs)


class CounterpartyAccountUpdate(LoginRequiredMixin,
                                UpdateView):
    """ update a counterpartys' bank account"""

    model = CounterpartyAccount
    template_name = 'transactions/bankaccount_update.html'
    fields = ['account', 'comment']


class CounterpartyAccountDelete(LoginRequiredMixin, DeleteView):
    """ delete a counterparty's account """

    model = CounterpartyAccount
    template_name = 'transactions/common_confirm_delete.html'

    def get_success_url(self):
        counterparty = self.object.counterparty
        return reverse_lazy('transactions:counterparty-detail',
                            kwargs={'pk': counterparty.pk})
