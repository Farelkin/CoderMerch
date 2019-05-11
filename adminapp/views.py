from products.models import ProductCategory, Product, ProductBySize, ProductImage
from django.shortcuts import get_object_or_404, render
from codermerch.settings import local_settings
from django.views.generic.list import ListView
from django.views.generic import TemplateView


def products(request):
    title = 'CoderMerch | Заказы'

    products_list = Product.objects.all()
    print(products_list)
    content = {
        'title': title,
        'products_list': products_list,

    }

    return render(request, 'adminapp/admin_products.html', content)


class AdminView(TemplateView):
    template_name = 'adminapp/admin.html'


class AdminOrdersView(TemplateView):
    template_name = 'adminapp/admin_orders.html'


class AdminUsersView(TemplateView):
    template_name = 'adminapp/admin_users.html'
