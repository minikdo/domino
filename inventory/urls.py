from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.ItemCreate.as_view(), name='create'),
    path('<int:pk>/update/', views.ItemUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.ItemDelete.as_view(), name='delete'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('inventory/add/', views.InventoryCreate.as_view(),
         name='inventory_create'),
    path('inventory/select/', views.inventory_select, name='inventory_select')
]
