from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Machine, Device, Service
from django.urls import reverse_lazy
import time


class IndexView(LoginRequiredMixin, ListView):
    """
    host list
    """
    template_name = 'machines/index.html'
    context_object_name = 'machines'
    
    def get_queryset(self):
        return Machine.objects.order_by('pk')
    

class DetailView(DetailView):
    """
    host details
    """
    model = Machine
    template_name = 'machines/detail.html'


class ServiceIndexView(LoginRequiredMixin, ListView):
    """
    service list
    """
    template_name = 'machines/service_index.html'
    context_object_name = 'services'
    model = Service
    ordering = '-date'
    paginate_by = 10
    

class ServiceCreate(LoginRequiredMixin, CreateView):
    """
    service add
    """
    model = Service
    fields = ['machine', 'date', 'description', 'device']

    def get_initial(self, **kwargs):
        return {'machine': self.request.GET.get("machine_id", None),
                'date': time.strftime('%Y-%m-%d')}


class ServiceUpdate(LoginRequiredMixin, UpdateView):
    """
    service update
    """
    model = Service
    fields = ['machine', 'date', 'description', 'device']
    
    
class ServiceDelete(LoginRequiredMixin, DeleteView):
    """
    service delete
    """
    model = Service

    def get_success_url(self):
        machine = self.object.machine
        return reverse_lazy('detail', kwargs={'pk': machine.pk})


class DeviceIndexView(LoginRequiredMixin, ListView):
    """
    component list
    """
    template_name = 'machines/device_index.html'
    context_object_name = 'device'
    model = Device
    paginate_by = 10
    ordering = '-date'


class DeviceDetailView(LoginRequiredMixin, DetailView):
    """
    component detail
    """
    model = Device
    template_name = 'machines/device_detail.html'


class DeviceCreate(LoginRequiredMixin, CreateView):
    """
    component add
    """
    model = Device
    fields = ['machine', 'date', 'type', 'name', 'price', 'company', 'invoice']

    def get_initial(self, **kwargs):
        return {'date': time.strftime('%Y-%m-%d')}

    
class DeviceUpdate(LoginRequiredMixin, UpdateView):
    """
    component update
    """
    model = Device
    fields = ['machine', 'date', 'type', 'name', 'price', 'company', 'invoice']
    
    
class DeviceDelete(LoginRequiredMixin, DeleteView):
    """
    component delete
    """
    model = Device
    success_url = reverse_lazy('device_index')
