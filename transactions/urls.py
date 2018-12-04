from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='transaction-index'),
    # path('add/', name='transaction-create'),
    # path('<int:pk>/update/', name='transaction-update'),
    # path('<int:pk>/delete/', name='transaction-delete'),
    path('counterparty/', views.CounterpartyIndexView.as_view(),
         name='counterparty-index'),
    path('counterparty/<int:pk>/', views.CounterpartyDetailView.as_view(),
         name='counterparty-detail'),
    path('counterparty/add/', views.CounterpartyCreate.as_view(),
         name='counterparty-create'),
    # path('counterparty/<int:pk>/update/', name='counterparty-update'),
    # path('counterparty/<int:pk>/delete/', name='counterparty-delete'),
    # path('bankaccount/', name='bankaccount-index'),
    path('bankaccount/add/', views.CounterpartyAccountCreate.as_view(),
         name='bankaccount-create'),
    # path('bankaccount/<int:pk>/update/', name='bankaccount-update'),
    # path('bankaccount/<int:pk>/delete/', name='bankaccount-delete'),
    # path('transactionfile/', name='transactionfile-index'),
    # path('transactionfile/add/', name='transactionfile-create'),
    # path('transactionfile/<int:pk>/update/', name='transactionfile-update'),
    # path('transactionfile/<int:pk>/delete/', name='transactionfile-delete'),
]
