from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import filters

from rest_auth.views import LoginView

from products.serializers import *
from products.models import *
from users.serializers import *
from basket.serializers import *
from users.models import CustomUser


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('api:rest_login', request=request, format=format),
        'logout': reverse('api:rest_logout', request=request, format=format),
        'register': reverse('api:rest_register', request=request,
                            format=format),
        'password reset': reverse('api:rest_password_reset', request=request,
                                  format=format),
        'password change': reverse('api:rest_password_change', request=request,
                                   format=format),
        'user details': reverse('api:rest_user_details', request=request,
                                format=format),
        'users': reverse('api:customuser-list', request=request,
                         format=format),
        'products': reverse('api:product-list', request=request,
                            format=format),
        'categories': reverse('api:productcategory-list', request=request,
                              format=format),
        'basket': reverse('api:basket-list', request=request, format=format),
    })


class CustomLogin(LoginView):

    def get_response(self):
        orginal_response = super().get_response()
        print(self.request.POST.get('remember_me', 'false'))
        if self.request.POST.get('remember_me', 'false') == 'false':
            self.request.session.set_expiry(0)
        return orginal_response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.filter(is_active=True)
    http_method_names = ['get', 'put', 'patch', 'head', 'delete', 'options']


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('keywords', 'name_product', 'category__name_category',)
    ordering_fields = ('name_product', 'price',)
    http_method_names = ['get', 'head', 'options']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance)
        return Response(serializer.data)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductSerializer(
            Product.objects.filter(category_id=instance.id), many=True)
        return Response(serializer.data)


class BasketViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BasketSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('datetime_added',)
    ordering = ['-datetime_added', ]

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):

        basket_product = Basket.objects.filter(user=self.request.user,
                                               product=serializer.data[
                                                   'product']).first()

        if not basket_product:
            serializer.save(user=self.request.user)
        else:
            basket_product.quantity += serializer.data['quantity']
            basket_product.save()
