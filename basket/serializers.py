from rest_framework import serializers
from .models import Basket


class BasketProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    name = serializers.StringRelatedField(source='product.product.name_product')
    size = serializers.StringRelatedField(source='product.size')
    image = serializers.ImageField(source='product.product.first_img', read_only= True)

    class Meta:
        model = Basket
        exclude = ('id', 'product', 'user', 'is_ordered')

