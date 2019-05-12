from django.db import models


class ProductCategory(models.Model):
    """КАТЕГОРИЯ ПРОДУКТА - тип товара (толстовка, футболка, аксессуары и т.д.)"""
    name_category = models.CharField(verbose_name='Категория продукта',
                                     max_length=40, unique=True, db_index=True)
    discount = models.PositiveSmallIntegerField(verbose_name='Процент скидки',
                                                default=0)
    is_active = models.BooleanField(verbose_name='Категория активна',
                                    default=True)

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Product(models.Model):
    """ПРОДУКТ - список всех продуктов, без учета размеров"""
    # Список категорий людей
    GENDER_CHOICES = (
        ('male', 'Мужское'),
        ('female', 'Женское')
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 related_name='product_category')
    name_product = models.CharField(verbose_name='Название товара',
                                    max_length=80, unique=True, db_index=True)

    logotype = models.CharField(verbose_name='Логотип товара (тема)',
                                max_length=30)
    gender = models.CharField(verbose_name='Категория людей или тип товара',
                              max_length=15,
                              choices=GENDER_CHOICES)
    color = models.CharField(verbose_name='Цвет', max_length=30)
    article = models.CharField(verbose_name='Артикл', max_length=15,
                               unique=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=8,
                                decimal_places=2, default=0)
    discount = models.PositiveSmallIntegerField(verbose_name='Процент скидки',
                                                default=0)
    description = models.TextField(verbose_name='Описание товара', blank=True)

    keywords = models.CharField(max_length=100, verbose_name=u"Ключевые слова",
                                blank=True, db_index=True)

    def __str__(self):
        return '{} ({})'.format(self.name_product, self.category.name_category)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    # получение всех картинок выбранного товара
    def get_img(self):
        lst = []
        item = self.prod_img.select_related()
        for img in item:
            lst.append(str(img.img_product))
        return lst

    # получение всех размеров выбранного товара
    def get_size(self):
        lis_size = {}
        item = self.prod_by_size.select_related()
        for one_size in item:
            lis_size[str(one_size.size)] = str(one_size.quantity)
        return lis_size

    @property
    def total_qty(self):
        return sum([i.quantity for i in self.prod_by_size.select_related()])


class ProductBySize(models.Model):
    """КОЛИЧЕСТВО ТОВАРОВ ПО РАЗМЕРАМ"""
    # Список возможных размеров товара
    PRODUCT_SIZE_CHOICES = (
        ('30', '30'), ('32', '32'), ('34', '34'),
        ('36', '36'), ('38', '38'), ('40', '40'),
        ('42', '42'), ('44', '44'), ('46', '46'),
        ('48', '48'), ('50', '50'), ('52', '52'),
        ('54', '54'), ('56', '56'), ('58', '58'),
    )

    product = models.ForeignKey(Product, related_name='prod_by_size',
                                on_delete=models.CASCADE)
    size = models.CharField(verbose_name='Размер', max_length=3,
                            choices=PRODUCT_SIZE_CHOICES)
    quantity = models.PositiveIntegerField(verbose_name='Количество на складе',
                                           default=0, )

    def __str__(self):
        return '{} ({})'.format(self.product.name_product, self.size)

    class Meta:
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товаров'


class ProductImage(models.Model):
    """ФОТОГРАФИИ ТОВАРОВ"""
    product = models.ForeignKey(Product, related_name='prod_img',
                                on_delete=models.CASCADE)
    img_product = models.ImageField(verbose_name='Фотография товара',
                                    max_length=255, upload_to='content')
 
    def __str__(self):
        return 'фотографии ({})'.format(self.product.name_product)

    class Meta:
        verbose_name = 'Фотографии товара'
        verbose_name_plural = 'Фотографии товаров'
