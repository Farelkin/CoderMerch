from .models import Product, ProductCategory
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    qty = serializers.IntegerField(source='total_qty', read_only=True)

    class Meta:
        model = Product
        fields = ('name_product', 'article', 'description', 'category', 'price', 'qty', )


class ProductCategorySerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(source='product_category', read_only=True, many=True)

    class Meta:
        model = ProductCategory
        fields = ('name_category', 'products')


class ProductDetailSerializer(serializers.ModelSerializer):
    sizes = serializers.DictField(source='get_size')

    class Meta:
        model = Product
        fields = ('name_product', 'sizes')

