from django import forms

from .models import DeviceType, Location


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
