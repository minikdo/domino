# from django.shortcuts import render
# from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Machine, Device, Service
from django.urls import reverse_lazy
import time


class IndexView(generic.ListView):
    """
    host list
    """
    template_name = 'machines/index.html'
    context_object_name = 'machines'
    
    def get_queryset(self):
        return Machine.objects.order_by('pk')
    

class DetailView(generic.DetailView):
    """
    host details
    """
    model = Machine
    template_name = 'machines/detail.html'


class ServiceIndexView(generic.ListView):
    """
    service list
    """
    template_name = 'machines/serwis_index.html'
    context_object_name = 'serwisy'
    model = Service
    ordering = '-date'
    paginate_by = 10
    

class ServiceCreate(CreateView):
    """
    service add
    """
    model = Service
    fields = ['machine', 'date', 'description', 'device']

    def get_initial(self, **kwargs):
        return {'machine': self.request.GET.get("machine_id", None),
                'date': time.strftime('%Y-%m-%d')}


class ServiceUpdate(UpdateView):
    """
    service update
    """
    model = Service
    fields = ['machine', 'date', 'description', 'device']
    
    
class ServiceDelete(DeleteView):
    """
    service delete
    """
    model = Service

    def get_success_url(self):
        machine = self.object.machine
        return reverse_lazy('detail', kwargs={'pk': machine.pk})


class DeviceIndexView(generic.ListView):
    """
    component list
    """
    template_name = 'machines/sprzet_index.html'
    context_object_name = 'sprzet'
    model = Device
    paginate_by = 10                                                        
    ordering = '-date'


class DeviceDetailView(generic.DetailView):
    """
    component detail
    """
    model = Device
    template_name = 'machines/sprzet_detail.html'


class DeviceCreate(CreateView):
    """
    component add
    """
    model = Device
    fields = ['machine', 'date', 'type', 'name', 'price', 'company', 'invoice']

    def get_initial(self, **kwargs):
        return {'date': time.strftime('%Y-%m-%d')}

    
class DeviceUpdate(UpdateView):
    """
    component update
    """
    model = Device
    fields = ['machine', 'date', 'type', 'name', 'price', 'company', 'invoice']
    
    
class DeviceDelete(DeleteView):
    """
    component delete
    """
    model = Device
    success_url = reverse_lazy('device_index')
