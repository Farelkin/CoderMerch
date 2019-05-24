from django.core.management.base import BaseCommand
from products.models import ProductCategory, Product, ProductBySize, \
    ProductImage
import json
import os
from django.core.files.images import ImageFile
from shutil import copyfile
from django.db import connection

# путь к файлу с данными продуктов
JSON_PATH = 'products/json'


def loadFromJSON(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r',
              encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        products_data = loadFromJSON('product_data')

        # удаляем все данные из таблиц
        Product.objects.all().delete()
        ProductBySize.objects.all().delete()
        ProductImage.objects.all().delete()
        ProductCategory.objects.all().delete()

        for i in (
                'ALTER SEQUENCE products_productcategory_id_seq RESTART WITH 1;',
                'ALTER SEQUENCE products_product_id_seq RESTART WITH 1;',
                'ALTER SEQUENCE products_productbysize_id_seq RESTART WITH 1;',
                'ALTER SEQUENCE products_productimage_id_seq RESTART WITH 1;',
        ):
            connection.cursor().execute(i)

        # фаилы выбивающиеся из общей системы названий, копирование его с переименованием
        copyfile(os.path.join('media/content/', 'woman/jackets', '4.png'),
                 os.path.join('media/content/', 'woman/jackets', 'c1-1.jpg'))
        copyfile(os.path.join('media/content/', 'woman/tshirts', 'wcp22.jpg'),
                 os.path.join('media/content/', 'woman/tshirts', 'wcp2-2.jpg'))
        copyfile(os.path.join('media/content/', 'woman/tshirts', 'wcp24.jpg'),
                 os.path.join('media/content/', 'woman/tshirts', 'wcp2-4.jpg'))
        copyfile(os.path.join('media/content/', 'man/tshirts', 'r1-1psd.jpg'),
                 os.path.join('media/content/', 'man/tshirts', 'r1-1.jpg'))

        for data in products_data:
            name_category = data['category']

            """Запись категорий продуктов в таблицу ProductCategory"""
            try:
                # проверяем наличие категории в таблице ProductCategory
                ProductCategory.objects.get(name_category=name_category)
            except (ProductCategory.DoesNotExist,):
                # если категории в таблице нет добавляем
                category = ProductCategory(name_category=name_category)
                category.save()

            """Запись данных о продукте в таблицу Product"""
            category = ProductCategory.objects.get(name_category=name_category)
            product = Product(
                category=category,
                name_product=data['name'],
                logotype=data['logotype'],
                gender=data['gender'],
                color=data['color'],
                article=data['article'],
                price=data['price'],
                description=data['description']
            )
            product.save()

            """Запись размеров продукта в таблицу ProductBySize"""
            product = Product.objects.get(name_product=data['name'])

            size_list = data['size_quantity']
            for size in size_list.keys():
                product_size = ProductBySize(
                    product=product,
                    size=size,
                    quantity=size_list[size]
                )
                product_size.save()

            """Запись картинок фотографий продукта в таблицу ProductImage"""
            print(data['product'])
            for i in range(1, 5):
                try:
                    path_img = 'content/' + data['product'] + f'-{i}.jpg'
                    ImageFile(open('media/' + path_img, "rb"))
                    product_img = ProductImage(
                        product=product,
                        img_product=path_img
                    )
                    product_img.save()
                except FileNotFoundError:
                    path_img = 'content/' + data['product'][:-1] + f'{i}.jpg'
                    ImageFile(open('media/' + path_img, "rb"))
                    product_img = ProductImage(
                        product=product,
                        img_product=path_img
                    )
                    product_img.save()
