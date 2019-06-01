from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'mainapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('account/', login_required(AccountView.as_view()), name='account'),
]
