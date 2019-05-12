from django.urls import path

from .views import *

app_name = 'adminapp'

urlpatterns = [
    path('', AdminMainView.as_view(), name='admin_main'),
    path('orders/', AdminOrdersView.as_view(), name='admin_orders'),
    path('products/', AdminProductsView.as_view(), name='admin_products'),
    path('users/', AdminUsersView.as_view(), name='admin_users'),
]
