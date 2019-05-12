from django.urls import path

from . import views

app_name = 'adminapp'

urlpatterns = [
    path('', views.AdminMainView.as_view(), name='admin'),
    path('admin_products/', views.AdminProductsView.as_view(), name='admin_products'),
    path('admin_orders/', views.AdminOrdersView.as_view(), name='admin_orders'),
    path('admin_users/', views.AdminUsersView.as_view(), name='admin_users'),
]

