from django.urls import path

from .views import *

app_name = 'basket'

urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
]
