from .models import Product, ProductCategory, ProductBySize, ProductImage, ProductsLike
from rest_framework import serializers


class ProductBySizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductBySize
        fields = ('size', 'quantity')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('img_product',)


class ProductSerializer(serializers.ModelSerializer):
    # qty = serializers.IntegerField(source='total_qty', read_only=True)

    category = serializers.HyperlinkedRelatedField(
        view_name='api:productcategory-detail',
        lookup_field='pk',
        many=False,
        read_only=False,
        queryset=ProductCategory.objects.all())

    name_category = serializers.CharField(source='category')

    url = serializers.HyperlinkedIdentityField(
        view_name='api:product-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Product
        fields = (
            'url',
            'article',
            'name_product',
            'category',
            'name_category',
            'description',
            'price',
            'discount',
            'main_img',
            'logotype',
            'gender',
            'color',
            'datetime_added',
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    sizes = ProductBySizeSerializer(source='prod_by_size', many=True, required=False, read_only=True)
    images = ProductImageSerializer(source='prod_img', many=True, required=False, read_only=True)
    category = serializers.HyperlinkedRelatedField(
        view_name='api:productcategory-detail',
        lookup_field='pk',
        many=False,
        read_only=False,
        queryset=ProductCategory.objects.all())
    url_similar_products = serializers.HyperlinkedIdentityField(
        view_name='api:product-similar',
        lookup_field='pk'
    )
    name_category = serializers.CharField(source='category')

    class Meta:
        model = Product
        fields = (
            'article',
            'name_product',
            'category',
            'name_category',
            'description',
            'price',
            'discount',
            'main_img',
            'images',
            'logotype',
            'gender',
            'color',
            'sizes',
            'datetime_added',
            'url_similar_products',
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:productcategory-detail',
        lookup_field='pk',
    )

    class Meta:
        model = ProductCategory
        exclude = ('id', 'is_active',)


class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        view_name='api:product-detail',
        lookup_field='pk',
        many=True,
        read_only=False,
        queryset=Product.objects.all())

    class Meta:
        model = ProductCategory
        fields = ('name_category', 'discount', 'products')


class ProductsLikeSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductsLike
        fields = ('user', 'product', 'is_active')