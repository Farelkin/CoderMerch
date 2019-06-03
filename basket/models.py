from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductBySize


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(ProductBySize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    @property
    def product_price(self):
        return self.product.product.price * self.quantity

    @property
    def total_price(self):
        products = Basket.objects.filter(user=self.user, is_ordered=False)
        return sum([x.product_price for x in products])
