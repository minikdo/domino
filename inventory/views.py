from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.db.models import Count
from django.conf import settings

from djatex import render_latex

from .models import Inventory, Item, Unit
from .forms import ItemForm, InventorySelectForm, SignUpForm
from .forms import ItemSearchForm
from .utils import shelf_counter, stats, get_total_items
from .mixins import InventorySessionMixin


@staff_member_required
def latex(request):
    inventory_id = request.session.get('inventory_id')

    items = get_total_items(inventory_id)
           
    inventory = Inventory.objects.get(pk=inventory_id)

    file_name = "rem_nr_{id}_z_{date}.pdf".format(
        id=inventory_id,
        date=inventory._creation_date())
    
    context = {'items': items,
               'counter': items.count(),
               'total_sum': stats(inventory_id),
               'inventory': inventory.shop.address,
               'date': inventory.created}
    
    return render_latex(request, file_name, 'inventory/item.tex',
                        error_template_name='inventory/error.html',
                        home_dir=settings.TEX_HOME,
                        context=context)
                                
                                    
class IndexView(LoginRequiredMixin, InventorySessionMixin, FormMixin,
                ListView):
    """ index """
    
    model = Item
    template_name = 'inventory/index.html'
    form_class = ItemForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_inventory'] = Inventory.objects.filter(
            pk=self.inventory).first()
        context['shelf_counter'] = shelf_counter(self.inventory,
                                                 self.request.user.id,
                                                 self.shelf)
        return context
                
    def get_queryset(self):
        query = Item.objects.filter(inventory=self.inventory,
                                    created_by=self.request.user)\
                                    .prefetch_related('make', 'unit')

        return query.order_by('-pk')[:5][::-1]  # reversed 5 last items

    def get_initial(self):
        try:
            last_choice = Item.objects.filter(created_by=self.request.user)\
                          .latest('pk')
        except Item.DoesNotExist:
            last_make = None
            last_unit = Unit.QTY_ID
        else:
            last_make = last_choice.make.id
            last_unit = last_choice.unit.id
            
        return {"make": last_make,
                "unit": last_unit,
                "quantity": 1}


class ItemCreate(LoginRequiredMixin, CreateView):
    """ add an item to the inventory """

    model = Item
    template_name = 'inventory/index.html'
    fields = ['make', 'price', 'quantity', 'unit']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.inventory_id = self.request.session['inventory_id']
        return super().form_valid(form)


class ItemUpdate(LoginRequiredMixin, UpdateView):
    """ update an item """

    model = Item
    fields = ['make', 'price', 'quantity', 'unit']
    template_name_suffix = '_update_form'
    

class ItemDelete(LoginRequiredMixin, DeleteView):
    """ delete an item """

    model = Item
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = '/'
    

class InventoryCreate(LoginRequiredMixin, CreateView):
    """ create an inventory session """

    model = Inventory
    fields = ['shop']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    
@login_required()
def inventory_select(request):
    """ select an inventory """
    # import pdb; pdb.set_trace()
    
    template = "inventory/inventory_select.html"
    form = InventorySelectForm()
    inventories = Inventory.objects.all()

    if not inventories:
        return redirect('inventory_create')
    
    last_inventory = inventories.latest('pk')
    
    if request.POST:
        request.session['inventory_id'] = request.POST.get('inventory')
        request.session['group_id'] = request.POST.get('group')

        return redirect('index')

    inventory = request.session.get('inventory_id', last_inventory.id)
    group = request.session.get('group_id', 1)
    form = InventorySelectForm({'inventory': inventory,
                                'group': group})

    return render(request, template, {"form": form,
                                      "inventories": inventories,
                                      "current_inventory": inventory})


class ItemSearch(LoginRequiredMixin, InventorySessionMixin, FormMixin,
                 ListView):
    """ item search """

    model = Item
    form_class = ItemSearchForm
    template_name = 'inventory/item_search.html'
    paginate_by = 50
    
    def get_queryset(self):
        query = Item.objects.filter(inventory=self.inventory)

        if self.myuser:
            query = query.filter(created_by=self.myuser)
        if self.make and self.make is not '':
            query = query.filter(make=self.make)
        if self.id and self.id is not '':
            query = query.filter(id=self.id)
        if self.price and self.price is not '':
            query = query.filter(price=self.price)
        if not self.show_all and not self.myuser and not self.make and\
           not self.price and self.shelf:
            query = query.filter(pk__gte=self.shelf)
            query = query.filter(created_by=self.request.user.id)

        self.item_num = query.count()
        query = query.prefetch_related('unit', 'make', 'created_by')\
                     .order_by('pk')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_inventory'] = Inventory.objects.filter(
            pk=self.inventory).first()
        context['shelf_counter'] = shelf_counter(self.inventory,
                                                 self.request.user.id,
                                                 self.shelf)

        context['item_num'] = self.item_num
        return context

    def get_initial(self):
        return {'make': self.make,
                'price': self.price,
                'myuser': self.myuser}
        
    def dispatch(self, request, *args, **kwargs):
        self.id = request.GET.get('id', None)
        self.make = request.GET.get('make', None)
        self.price = request.GET.get('price', None)
        self.myuser = request.GET.get('myuser', None)
        self.show_all = request.GET.get('show_all', None)
        
        return super().dispatch(request, *args, **kwargs)


@login_required()
def shelf_reset(request):
    """ update shelf counter """

    if request.session.get('inventory_id') is None:
            return redirect('inventory_select')

    try:
        last_item_id = Item.objects.filter(created_by=request.user,
                                           inventory_id=request.session.get(
                                               'inventory_id')).last().pk
    except Item.DoesNotExist:
        request.session['shelf_id'] = 0
    else:
        request.session['shelf_id'] = last_item_id + 1
    
    return redirect('index')


@method_decorator(staff_member_required, name='dispatch')
class Stats(TemplateView):
    """ sums and statistics """

    template_name = 'inventory/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        items = Item.objects.filter(inventory_id=self.inventory)
        
        context['sum'] = stats(self.inventory)
        context['count'] = items.count()
        context['count_by_user'] = items\
                                   .values('created_by__username')\
                                   .annotate(count=Count('pk'))
        context['current_inventory'] = items.first().inventory

        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.inventory = request.session.get('inventory_id')

        if not self.inventory:
            return redirect('inventory_select')

        return super().dispatch(request, *args, **kwargs)


def register(request):
    """ registration form """
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username,
                                password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
        
    context = {'form': form}
    
    return render(request, 'registration/register.html', context)
