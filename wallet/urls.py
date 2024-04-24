from django.urls import path
from . import views

urlpatterns = [
    path('get_wallets/', views.wallet_list, name='wallet_list'),
    path('<int:pk>/add_funds/', views.add_funds, name='add_funds'), 
    path('transactions/', views.transactions, name='transactions'), 
]