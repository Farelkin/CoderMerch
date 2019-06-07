from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
]
