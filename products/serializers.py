from .models import Product, ProductCategory, ProductBySize, ProductImage, ProductsLike
from rest_framework import serializers


class ProductBySizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductBySize
        fields = ('id', 'size', 'quantity')


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
    product_id = serializers.IntegerField(source='product.id')
    product_url = serializers.HyperlinkedRelatedField(source='product',
                                                      view_name='api:product-detail',
                                                      lookup_field='pk',
                                                      many=False,
                                                      read_only=True,
                                                      )
    article = serializers.StringRelatedField(
        source='product.article')
    name_product = serializers.StringRelatedField(
        source='product.name_product')
    category = serializers.HyperlinkedRelatedField(
        source='product.category',
        view_name='api:productcategory-detail',
        lookup_field='pk',
        many=False,
        read_only=True,
    )
    name_category = serializers.CharField(source='product.category',
                                          read_only=True)

    description = serializers.StringRelatedField(
        source='product.description')
    price = serializers.DecimalField(source='product.price',
                                     max_digits=10, decimal_places=2,
                                     read_only=True)
    discount = serializers.IntegerField(source='product.discount',
                                        read_only=True)
    main_img = serializers.ImageField(source='product.main_img',
                                      read_only=True)
    logotype = serializers.StringRelatedField(
        source='product.logotype',
        read_only=True)
    gender = serializers.StringRelatedField(source='product.gender',
                                            read_only=True)
    color = serializers.StringRelatedField(source='product.color',
                                           read_only=True)

    class Meta:
        model = ProductsLike
        exclude = ('product', 'user')
