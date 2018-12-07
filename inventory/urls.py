from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.ItemSearch.as_view(), name='item_search'),
    path('add/', views.ItemCreate.as_view(), name='create'),
    path('<int:pk>/update/', views.ItemUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.ItemDelete.as_view(), name='delete'),
    path('inventory/add/', views.InventoryCreate.as_view(),
         name='inventory_create'),
    path('inventory/select/', views.inventory_select, name='inventory_select'),
    path('shelf/reset', views.shelf_reset, name='shelf_reset'),
    path('stats/', views.Stats.as_view(), name='stats'),
    path('latex/', views.latex, name='latex'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
