from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings

from djatex import render_latex
from num2words import num2words

from .forms import ContractForm


class Form(LoginRequiredMixin, FormView):

    form_class = ContractForm
    template_name = 'gold/form.html'
    

@login_required
def latex(request, **kwargs):
    """Generate an invoice in PDF"""

    number = request.POST.get('number', None)
    date = request.POST.get('date', None)
    seller = request.POST.get('seller', None)
    weight = request.POST.get('weight', None)
    price = request.POST.get('price', None)
    
    file_name = "umowa_{number}_z_{date}.pdf".format(
        number=number, date=date)

    context = {'number': number,
               'date': date,
               'seller': seller,
               'weight': weight,
               'price': price,
               'price_words': num2words(price, lang='pl')
    }
    
    return render_latex(request, file_name, 'gold/contract.tex',
                        error_template_name='gold/error.html',
                        home_dir=settings.TEX_HOME,
                        context=context)
