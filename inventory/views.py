from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Inventory, Item
from .forms import ItemForm, InventorySelectForm, SignUpForm, ItemSearchForm
from .utils import shelf_counter, stats


@method_decorator(login_required, name='dispatch')
class IndexView(FormMixin, ListView):
    """ index """
    
    model = Item
    template_name = 'inventory/index.html'
    form_class = ItemForm
    
    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['current_inventory'] = Inventory.objects.filter(
            pk=self.inventory).first()
        context['shelf_counter'] = shelf_counter(self.inventory,
                                                 self.request.user.id,
                                                 self.shelf)
        return context
                
    def get_queryset(self):
        query = Item.objects.filter(inventory=self.inventory,
                                    created_by=self.request.user)

        return query.order_by('-pk')[:5][::-1]

    def get_initial(self):
        try:
            last_choice = Item.objects.filter(created_by=self.request.user)
            last_choice = last_choice.latest('pk')
        except:
            last_make = 1
            last_unit = 1
        else:
            last_make = last_choice.make.id
            last_unit = last_choice.unit.id
            
        return {"make": last_make,
                "unit": last_unit,
                "quantity": 1}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(session_data={'inventory_id': self.inventory,
                                    'group_id': self.group})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.inventory = request.session.get('inventory_id')
        self.group = request.session.get('group_id')
        self.shelf = request.session.get('shelf_id')
        
        if self.inventory is None:
            return redirect('inventory_select')

        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ItemCreate(CreateView):
    """ add an item to the inventory """

    model = Item
    template_name = 'inventory/index.html'
    fields = ['make', 'price', 'quantity', 'unit']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.inventory_id = self.request.session['inventory_id']
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ItemUpdate(UpdateView):
    """ update an item """

    model = Item
    fields = ['make', 'price', 'quantity', 'unit']
    template_name_suffix = '_update_form'
    

@method_decorator(login_required, name='dispatch')
class ItemDelete(DeleteView):
    """ delete an item """

    model = Item
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = '/'
    

@method_decorator(login_required, name='dispatch')
class InventoryCreate(CreateView):
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
                                      "current_inventory": last_inventory})


@method_decorator(login_required, name='dispatch')
class ItemSearch(FormMixin, ListView):
    """ item search """

    model = Item
    template_name = 'inventory/item_search.html'
    form_class = ItemSearchForm
    paginate_by = 10
    
    def get_queryset(self):
        query = Item.objects.filter(inventory=self.inventory,
                                    created_by=self.request.user)

        if self.make:
            query = query.filter(make=self.make)
        if self.price:
            query = query.filter(price=self.price)
        if not self.make and not self.price and self.shelf:
            query = query.filter(pk__gte=self.shelf)

        self.item_num = query.count()
        query = query.order_by('pk')
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
                'price': self.price}
        
    def dispatch(self, request, *args, **kwargs):
        self.inventory = request.session.get('inventory_id')

        self.make = request.GET.get('make', None)
        self.price = request.GET.get('price', None)

        if not self.inventory:
            return redirect('inventory_select')

        self.shelf = request.session.get('shelf_id')

        return super().dispatch(request, *args, **kwargs)


@login_required()
def shelf_reset(request):
    """ update shelf counter """

    last_item_id = Item.objects.filter(created_by=request.user,
                                       inventory_id=request.session.get(
                                           'inventory_id')).last().id
    request.session['shelf_id'] = last_item_id + 1
    
    return redirect('index')


@method_decorator(login_required, name='dispatch')
class Stats(ListView):
    """ sums and statistics """

    model = Item
    template_name = 'inventory/stats.html'

    def get_queryset(self):
        return stats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counts'] = Item.objects.filter(
            inventory_id=self.inventory).count()
        return context
    

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
