from django.urls import path
#from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'gold'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]