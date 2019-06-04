from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(source='order_product', read_only=True, required=False, many=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        exclude = ('user', 'is_active',)

