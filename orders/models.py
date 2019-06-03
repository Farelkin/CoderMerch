from django.db import models
from django.contrib.auth import get_user_model
from basket.models import Basket


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    time_ordered = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING)
    delivery = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class OrderUnits(models.Model):
    product = models.ForeignKey(Basket, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_product')

    def __str__(self):
        return self.product.product.product.name_product



# Create your models here.
