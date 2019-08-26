# from django.views.generic import FormView
from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings

from djatex import render_latex
from num2words import num2words

from .forms import ContractForm


@login_required
def contract_view(request):

    if request.method == 'POST':
        form = ContractForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']
            date = form.cleaned_data['date']
            seller = form.cleaned_data['seller']
            weight = form.cleaned_data['weight']
            price = form.cleaned_data['price']

            file_name = "umowa_{number}_z_{date}.pdf".format(
                number=number, date=date)

            form_context = {'number': number,
                            'date': date,
                            'seller': seller,
                            'weight': weight,
                            'price': price,
                            'price_words': num2words(price, lang='pl')}

            return render_latex(request, file_name, 'gold/contract.tex',
                                error_template_name='gold/error.html',
                                home_dir=settings.TEX_HOME,
                                context=form_context)
    else:
        form = ContractForm()
    context = {'form': form}
    return render(request, 'gold/form.html', context)
