from django.urls import path

from .views import *

app_name = 'basket'

urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
    path('order-done/', OrderDoneView.as_view(), name='order_done'),
]
