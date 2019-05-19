from .models import Product, ProductCategory
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    # qty = serializers.IntegerField(source='total_qty', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'article',
            'name_product',
            'description',
            'price',
            'discount',
            'main_img',
            'logotype',
            'gender',
            'color'
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    sizes = serializers.DictField(source='get_size')

    class Meta:
        model = Product
        fields = (
            'id',
            'article',
            'name_product',
            'description',
            'price',
            'discount',
            'main_img',
            'logotype',
            'gender',
            'color',
            'sizes'
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ('is_active',)


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    products = serializers.ListField(source='get_products')

    class Meta:
        model = ProductCategory
        fields = ('id', 'name_category', 'discount', 'products')
