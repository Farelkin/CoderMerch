from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(source='order_product', many=True, read_only=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

