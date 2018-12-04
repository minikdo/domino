# from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Transaction, Counterparty


class IndexView(LoginRequiredMixin, ListView):
    """ transaction list """

    model = Transaction
    template_name = 'transactions/index.html'


class CounterpartyIndexView(LoginRequiredMixin, ListView):
    """ counterparty list """

    model = Counterparty
    template_name = 'transactions/counterparty_index.html'


class CounterpartyDetailView(LoginRequiredMixin, DetailView):
    """ counterparty details """

    model = Counterparty
    template_name = 'transactions/counterparty_detail.html'


class CounterpartyCreate(LoginRequiredMixin, CreateView):
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
