from django import forms

from .models import DeviceType, Location, Service


class DeviceSearchForm(forms.Form):
    """ device search form """

    device_type = forms.ModelChoiceField(DeviceType.objects.all(),
                                         required=False)
    location = forms.ModelChoiceField(Location.objects.all(),
                                      required=False)


class MachineSetupForm(forms.Form):
    """ ansible setup form """

    file_field = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': True}))


class ServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {'description': forms.Textarea(attrs={'cols': 60,
                                                        'rows': 4}),
                   'machine': forms.Select(attrs={'autofocus': True})}
