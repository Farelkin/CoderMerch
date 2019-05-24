import django_filters
from products.models import Product


class AdminProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = ['gender']


