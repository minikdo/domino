# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings

from djatex import render_latex

from .models import Invoice, InvoiceItem, Customer
from .forms import InvoiceForm, InvoiceItemForm, CustomerSearchForm
from .utils import SumItems
from transactions.mixins import CreatedByMixin


@login_required
def latex(request, **kwargs):
    """Generate an invoice in PDF"""
    
    invoice = kwargs['invoice']

    invoice_data = Invoice.objects.get(pk=invoice)
    items = InvoiceItem.objects.filter(invoice=invoice)
           
    file_name = "faktura_{id}_z_{date}.pdf".format(
        id=invoice, date=invoice_data.issued)
    
    context = {'invoice': invoice_data,
               'items': items,
               'total': SumItems(invoice)}
    
    return render_latex(request, file_name, 'invoices/invoice.tex',
                        error_template_name='invoices/error.html',
                        home_dir=settings.TEX_HOME,
                        context=context)


class IndexView(LoginRequiredMixin, ListView):
    """List of invoices"""

    model = Invoice
    template_name = 'invoices/index.html'
    
    def get_queryset(self):
        queryset = Invoice.objects.filter(created_by=self.request.user)
        return queryset


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    """Invoice detail"""

    model = Invoice
    template_name = 'invoices/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        invoice = self.kwargs['pk']
        items = InvoiceItem.objects.filter(invoice=invoice)

        context['items'] = items
        context['total'] = SumItems(invoice)
        
        return context
    

class InvoiceCreateView(LoginRequiredMixin, CreatedByMixin, CreateView):
    """Create an invoice"""

    model = Invoice
    template_name = 'invoices/create.html'
    form_class = InvoiceForm

    def get_initial(self):
        return {'customer': self.kwargs['customer']}
    

class InvoiceUpdateView(LoginRequiredMixin, CreatedByMixin, UpdateView):
    """Update an invoice"""

    model = Invoice
    template_name = 'invoices/create.html'
    form_class = InvoiceForm
    

class InvoiceItemCreateView(LoginRequiredMixin, CreateView):
    """Create an invoice item"""

    model = InvoiceItem
    template_name = 'invoices/invoice_item_create.html'
    form_class = InvoiceItemForm
    
    def get_initial(self):
        return {'invoice': self.kwargs['invoice']}


class InvoiceItemUpdateView(LoginRequiredMixin, UpdateView):
    """Update an invoice item"""

    model = InvoiceItem
    template_name = 'invoices/invoice_item_create.html'
    form_class = InvoiceItemForm


class InvoiceItemDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an invoice item"""

    model = InvoiceItem
    template_name = 'invoices/_confirm_delete.html'

    def get_success_url(self):
        invoice = self.object.invoice
        return reverse_lazy('invoices:detail', kwargs={'pk': invoice.pk})


class CustomerIndexView(LoginRequiredMixin, FormMixin, ListView):
    """List of customers"""

    model = Customer
    template_name = 'invoices/customer_index.html'
    ordering = ['company', 'name']
    form_class = CustomerSearchForm

    def get_queryset(self):
        customers = Customer.objects.all()

        name = self.request.GET.get('name', None)

        if name and name is not '':
            customers = customers.filter(
                Q(name__icontains=name) |
                Q(company__icontains=name)
            )
        
        return customers
    

class CustomerDetailView(LoginRequiredMixin, DetailView):
    """Customer details"""
    
    model = Customer
    template_name = 'invoices/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['invoices'] = Invoice.objects.filter(
            customer=self.kwargs['pk']
        )
        
        return context

    
class CustomerCreateView(LoginRequiredMixin, CreatedByMixin, CreateView):
    """Create a customer"""

    model = Customer
    template_name = 'invoices/customer_create.html'
    fields = ['company', 'name', 'street', 'city',
              'postal_code', 'tax_id', 'email', 'phone']
    

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """Update a customer"""

    model = Customer
    template_name = 'invoices/customer_update.html'
    fields = ['company', 'name', 'street', 'city',
              'postal_code', 'tax_id', 'email', 'phone']


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a customer"""

    model = Customer
    template_name = 'invoices/_confirm_delete.html'
