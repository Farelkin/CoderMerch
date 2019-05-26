from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import filters

from rest_auth.views import LoginView
from rest_framework.decorators import action

from products.serializers import *
from products.models import *
from users.serializers import *
from basket.serializers import *
from users.models import CustomUser

from django.shortcuts import get_object_or_404


class ActionBasedPermission(permissions.AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """

    def has_permission(self, request, view):
        for c_class, actions in getattr(view, 'action_permissions',
                                        {}).items():
            if view.action in actions:
                return c_class().has_permission(request, view)
        return False


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'login': reverse('api:rest_login', request=request, format=format),
        'login-vk': request.build_absolute_uri('/accounts/vk/login/'),
        'login-github': request.build_absolute_uri('/accounts/github/login/'),
        'connecnt social account': request.build_absolute_uri(
            '/accounts/social/connections/'),
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
        'like': reverse('api:like-list', request=request, format=format),
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
    queryset = CustomUser.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('email', 'first_name', 'last_name', 'email')
    ordering_fields = ('email', 'last_name', 'first_name', 'is_active')
    ordering = ['-is_active', ]
    http_method_names = ['get', 'put', 'patch', 'head', 'delete', 'options']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomUserListSerializer(page, many=True,
                                                  context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = CustomUserListSerializer(queryset, many=True,
                                              context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAdminUser: ['update', 'partial_update', 'destroy',
                                  'create'],
        permissions.AllowAny: ['list', 'retrieve', 'get_similar']
    }

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('keywords', 'name_product', 'category__name_category',)
    ordering_fields = ('name_product', 'price', 'id')

    def get_queryset(self):
        queryset = self.queryset
        gender = self.request.query_params.get('gender', None)
        category = self.request.query_params.get('category', None)

        if gender is not None:
            queryset = queryset.filter(gender=gender)
        if category is not None:
            tmp = queryset.filter(category__name_category=category)
            if tmp:
                queryset = tmp

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance,
                                             context={'request': request})
        return Response(serializer.data)

    @action(detail=True, url_path='similar', url_name='similar')
    def get_similar(self, request, *args, **kwargs):

        instance = self.get_object()
        similar_queryset = Product.objects.filter(
            category__name_category=instance.category, gender=instance.gender) \
                               .exclude(id=instance.id).order_by('?')[0:4]
        serializer = ProductSerializer(similar_queryset, many=True,
                                       context={'request': request})
        return Response(serializer.data)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAdminUser: ['update', 'partial_update', 'destroy',
                                  'create'],
        permissions.AllowAny: ['list', 'retrieve']
    }
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductCategoryDetailSerializer(instance,
                                                     context={
                                                         'request': request})
        return Response(serializer.data)


class BasketViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BasketProductSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('datetime_added',)
    ordering = ['-datetime_added', ]

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        product_by_size = get_object_or_404(ProductBySize,
                                            pk=self.request.data[
                                                'product_by_size_id'])

        basket_product = Basket.objects.filter(user=self.request.user,
                                               product_id=product_by_size).first()

        if not basket_product:
            serializer.save(user=self.request.user, product=product_by_size)
        else:
            basket_product.quantity += serializer.data['quantity']
            basket_product.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        product_by_size = get_object_or_404(ProductBySize,
                                            pk=instance.product.pk)
        serializer.save(user=self.request.user, product=product_by_size)


class ProductsLikeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductsLikeSerializer
    http_method_names = ['get', 'post', 'head', 'delete', 'options']

    def get_queryset(self):
        return ProductsLike.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):

        product = get_object_or_404(Product,
                                    pk=self.request.data['product_id'])

        like_product = ProductsLike.objects.filter(user=self.request.user,
                                                   product=product).first()

        if not like_product:
            serializer.save(user=self.request.user, product=product)
