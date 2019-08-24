from django.urls import path
from django.http import HttpResponse
#from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = 'gold'

urlpatterns = [
    path('', views.Form.as_view(), name='form'),
    path('latex/', views.latex, name='latex'),
]

