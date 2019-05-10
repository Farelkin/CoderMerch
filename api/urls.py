from django.urls import include, path
from rest_framework import routers
from api.views import *

from . import views
from api.views import CustomLogin

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', views.api_root),
    path('login/', CustomLogin.as_view(), name='rest_login'),
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]

urlpatterns += router.urls
