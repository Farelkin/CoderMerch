from django.urls import path

from .views import *

app_name = 'products'

urlpatterns = [
    path('man/', ManProductsView.as_view(), name='man'),
    path('woman/', WomanProductsView.as_view(), name='woman'),
    path('like/', LikeView.as_view(), name='like'),
    path('<int:pk>/', ProductView.as_view(), name='product'),
]
