from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, \
    FormMixin, FormView
from django.urls import reverse_lazy

from .models import Machine, Device, Service
from .forms import DeviceSearchForm, MachineSetupForm, ServiceForm

import time


class MachineIndex(LoginRequiredMixin, ListView):
    """
    host list
    """
    template_name = 'machines/index.html'
    context_object_name = 'machines'

    def get_queryset(self):
        return Machine.objects.prefetch_related('location').order_by('pk')


class MachineDetail(DetailView):
    """
    host details
    """
    model = Machine
    template_name = 'machines/detail.html'
    queryset = Machine.objects.prefetch_related('device').all()


class MachineCreate(CreateView):
    """
    create a host
    """
    model = Machine
    fields = ['name', 'location']


class MachineUpdate(UpdateView):
    """
    edit machine
    """
    model = Machine
    fields = '__all__'


class MachineDelete(DeleteView):
    """
    remove a host
    """
    model = Machine
    success_url = reverse_lazy('machines:index')


class ServiceIndexView(LoginRequiredMixin, ListView):
    """
    service list
    """
    template_name = 'machines/service_index.html'
    context_object_name = 'services'
    paginate_by = 25

    def get_queryset(self):
        query = Service.objects.prefetch_related('machine', 'device')\
                .all()
        return query.order_by('-date')


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
    # fields = ['machine', 'date', 'description', 'device']
    form_class = ServiceForm


class ServiceDelete(LoginRequiredMixin, DeleteView):
    """
    service delete
    """
    model = Service

    def get_success_url(self):
        machine = self.object.machine
        return reverse_lazy('machines:detail', kwargs={'pk': machine.pk})


class DeviceIndexView(LoginRequiredMixin, FormMixin, ListView):
    """
    component list
    """
    template_name = 'machines/device_index.html'
    form_class = DeviceSearchForm
    context_object_name = 'device'
    model = Device
    paginate_by = 25

    def get_queryset(self):
        query = Device.objects.prefetch_related('type', 'location').all()

        if self.device_type:
            query = query.filter(type=self.device_type)
        if self.location:
            query = query.filter(location=self.location)

        return query.order_by('-date')

    def get_initial(self):
        initials = {}

        if self.device_type:
            initials['device_type'] = self.device_type
        if self.location:
            initials['location'] = self.location

        return initials

    def dispatch(self, request, *args, **kwargs):

        self.device_type = request.GET.get('device_type', None)
        self.location = request.GET.get('location', None)
        return super().dispatch(request, *args, **kwargs)


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
    fields = ['type', 'location', 'date', 'name', 'price', 'company',
              'invoice', 'machine']

    def get_initial(self, **kwargs):
        return {'date': time.strftime('%Y-%m-%d')}


class DeviceUpdate(LoginRequiredMixin, UpdateView):
    """
    component update
    """
    model = Device
    fields = ['type', 'location', 'date', 'name', 'price', 'company',
              'invoice', 'machine']


class DeviceDelete(LoginRequiredMixin, DeleteView):
    """
    component delete
    """
    model = Device
    success_url = reverse_lazy('machines:device_index')


class MachineSetupUpload(FormView):
    """ upload ansile setup json """

    form_class = MachineSetupForm
    success_url = reverse_lazy('machines:index')
    template_name = 'machines/setup_upload.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')

        if form.is_valid():
            for f in files:
                import json
                str = f.file.read().decode()
                j = json.loads(str)
                if 'failed' in j:
                    continue
                fqdn = j['ansible_facts']['ansible_fqdn']

                try:
                    obj = Machine.objects.get(FQDN=fqdn)
                except Machine.DoesNotExist:
                    return self.form_invalid(form)

                obj.date = j['ansible_facts']['ansible_date_time']['date']
                obj.form = j['ansible_facts']['ansible_form_factor']
                obj.bios = j['ansible_facts']['ansible_bios_date']
                obj.prod = j['ansible_facts']['ansible_product_name']
                obj.vendor = j['ansible_facts']['ansible_system_vendor']
                obj.OS = "%s %s" % (j['ansible_facts']['ansible_distribution'],
                                    j['ansible_facts']['ansible_distribution_version'])  # noqa
                obj.kernel = j['ansible_facts']['ansible_kernel']
                obj.CPU = j['ansible_facts']['ansible_processor'][0]
                obj.cores = j['ansible_facts']['ansible_processor_cores']
                obj.arch = j['ansible_facts']['ansible_architecture']
                obj.mem = j['ansible_facts']['ansible_memtotal_mb']
                # obj.disk = j ['ansible_facts']['ansible_devices']['sda']['model']  # noqa
                obj.IPs = ', '.join(j['ansible_facts']['ansible_all_ipv4_addresses'])  # noqa
                obj.gateway = j['ansible_facts']['ansible_default_ipv4']['gateway'],  # noqa
                obj.gate_iface =j['ansible_facts']['ansible_default_ipv4']['interface']  # noqa

                obj.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
