from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from dal.autocomplete import Select2ListView

from .models import Transaction, Counterparty, CounterpartyAccount
from .forms import CounterpartyAccountCreateForm, CounterpartySearch,\
    TransactionForm
from .mixins import CreatedByMixin


class IndexView(LoginRequiredMixin, ListView):
    """ transaction list """

    model = Transaction
    template_name = 'transactions/index.html'
    

class TransactionCreate(LoginRequiredMixin, CreatedByMixin, CreateView):
    """ create transaction """

    model = Transaction
    template_name = 'transactions/transaction_create.html'
    form_class = TransactionForm

    def get_initial(self, **kwargs):
        return {'counterparty_account': self.kwargs['bankaccount'],
                'transaction_type': 110,
                'transaction_classification': 51}
    
    
class CounterpartyIndexView(LoginRequiredMixin, FormMixin, ListView):
    """ counterparty list """

    model = Counterparty
    ordering = ['name']
    template_name = 'transactions/counterparty_index.html'
    form_class = CounterpartySearch

    def get_queryset(self):
        queryset = Counterparty.objects.all()

        self.name = self.request.GET.get('name', None)
        self.tax_id = self.request.GET.get('tax_id', None)
        
        if self.name and self.name is not '':
            queryset = queryset.filter(
                name__icontains=self.name)
        if self.tax_id and self.name is not '':
            queryset = queryset.filter(
                tax_id__icontains=self.tax_id)

        return queryset.order_by('name')

    def get_initial(self):
        return {'name': self.name,
                'tax_id': self.tax_id}


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
