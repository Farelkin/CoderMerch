from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from orders.serializers import OrderSerializer
from orders.models import Order, OrderUnits
from basket.models import Basket
from rest_framework import status


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        products_in_basket = Basket.objects.filter(user=self.request.user, is_ordered=False)
        if not products_in_basket:
            return Response(status=status.HTTP_204_NO_CONTENT)
        new_order = Order(user=self.request.user, delivery_id=serializer.data['delivery'])
        new_order.save()
        for i in products_in_basket:
            i.is_ordered = True
            i.save()
            new_order_item = OrderUnits(product=i, order=new_order)
            new_order_item.save()

# Create your views here.
