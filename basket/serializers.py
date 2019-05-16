from rest_framework import serializers
from .models import Basket


class BasketSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='product.product.name_product')
    size = serializers.StringRelatedField(source='product.size')

    class Meta:
        model = Basket
        exclude = ('id', 'user', 'is_ordered')
