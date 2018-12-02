# from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Transaction


class IndexView(LoginRequiredMixin, TemplateView):
    """ transaction list """

    model = Transaction
    template_name = 'transactions/index.html'
