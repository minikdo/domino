from django.urls import path
from django.http import HttpResponse
#from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = 'gold'

urlpatterns = [
    path('', views.contract_view, name='form'),
]

