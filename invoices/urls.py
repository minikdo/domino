from django.urls import path

from . import views

app_name = 'invoices'

urlpatterns = [
    # Invoices
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='detail'),
    path('<int:customer>/add/', views.InvoiceCreateView.as_view(),
         name='create'),
    path('<int:pk>/update/', views.InvoiceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='delete'),
    # Invoice Item
    path('item/<int:invoice>/add/', views.InvoiceItemCreateView.as_view(),
         name='invoice-item-create'),
    path('item/<int:pk>/update/', views.InvoiceItemUpdateView.as_view(),
         name='invoice-item-update'),
    path('item/<int:pk>/delete/', views.InvoiceItemDeleteView.as_view(),
         name='invoice-item-delete'),
    # Customers
    path('customer/', views.CustomerIndexView.as_view(),
         name='customer-index'),
    path('customer/<int:pk>/', views.CustomerDetailView.as_view(),
         name='customer-detail'),
    path('customer/add/', views.CustomerCreateView.as_view(),
         name='customer-create'),
    path('customer/<int:pk>/update/', views.CustomerUpdateView.as_view(),
         name='customer-update'),
    path('customer/<int:pk>/delete/', views.CustomerDeleteView.as_view(),
         name='customer-delete'),
    # Generate an invoice
    path('latex/<int:invoice>/', views.latex, name='latex'),
    # path('', views.as_view(), name=''),
]
