from django.urls import path
from django.views.generic import RedirectView
from . import views


app_name = 'adminapp'

urlpatterns = [
    path('', views.AdminMainView.as_view(), name='admin_main'),
    path('admin_products/', RedirectView.as_view(url='/myadmin/admin_products/all/', permanent=True)),
    path('admin_products/<str:pk>/', views.nav_filter_bar, name='admin_products'),
    # path('admin_products/category/<int:pk>/', views.AdminProductsView.as_view(), name='category'),
    # path('admin_products/gender/<int:pk>/', views.AdminProductsView.as_view(), name='gender'),
    path('admin_products_filter/', views.AdminProductsView.as_view(), name='somefilter'),
    path('admin_orders/', views.AdminOrdersView.as_view(), name='admin_orders'),
    path('admin_users/', views.AdminUsersView.as_view(), name='admin_users'),

]
