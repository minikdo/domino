from django.urls import path
from . import views

app_name = 'machines'

urlpatterns = [
    path('', views.MachineIndex.as_view(), name='index'),
    path('<int:pk>/', views.MachineDetail.as_view(), name='detail'),
    path('add/', views.MachineCreate.as_view(), name='create'),
    path('<int:pk>/update/', views.MachineUpdate.as_view(), name='update'),
    path('<int:pk>/del/', views.MachineDelete.as_view(),
         name='delete'),
    path('service/', views.ServiceIndexView.as_view(), name='service_index'),
    path('service/add/', views.ServiceCreate.as_view(), name='service_create'),
    path('service/<int:pk>/del/', views.ServiceDelete.as_view(),
         name='service_delete'),
    path('service/<int:pk>/update/', views.ServiceUpdate.as_view(),
         name='service_update'),
    path('device/', views.DeviceIndexView.as_view(), name='device_index'),
    path('device/<int:pk>/', views.DeviceDetailView.as_view(),
         name='device_detail'),
    path('device/add/', views.DeviceCreate.as_view(), name='device_create'),
    path('device/<int:pk>/del/', views.DeviceDelete.as_view(),
         name='device_delete'),
    path('device/<int:pk>/update/', views.DeviceUpdate.as_view(),
         name='device_update'),
]
