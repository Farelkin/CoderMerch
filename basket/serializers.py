from rest_framework import serializers
from .models import Basket


class BasketProductSerializer(serializers.ModelSerializer):
    product_by_size_id = serializers.IntegerField(source='product.id')
    product_url = serializers.HyperlinkedRelatedField(source='product.product',
                                                      view_name='api:product-detail',
                                                      lookup_field='pk',
                                                      many=False,
                                                      read_only=True,
                                                      )
    article = serializers.StringRelatedField(
        source='product.product.article')
    name_product = serializers.StringRelatedField(
        source='product.product.name_product')
    category = serializers.HyperlinkedRelatedField(
        source='product.product.category',
        view_name='api:productcategory-detail',
        lookup_field='pk',
        many=False,
        read_only=True,
    )
    name_category = serializers.CharField(source='product.product.category', read_only=True)

    description = serializers.StringRelatedField(
        source='product.product.description')
    price = serializers.DecimalField(source='product.product.price',
                                     max_digits=10, decimal_places=2,
                                     read_only=True)
    discount = serializers.IntegerField(source='product.product.discount',
                                        read_only=True)
    main_img = serializers.ImageField(source='product.product.main_img',
                                      read_only=True)
    logotype = serializers.StringRelatedField(
        source='product.product.logotype',
        read_only=True)
    gender = serializers.StringRelatedField(source='product.product.gender',
                                            read_only=True)
    color = serializers.StringRelatedField(source='product.product.color',
                                           read_only=True)
    size = serializers.StringRelatedField(source='product.size')

    class Meta:
        model = Basket
        exclude = ('id', 'product', 'user', 'is_ordered')
