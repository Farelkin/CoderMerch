from django.views.generic import TemplateView
from products.models import Product, ProductImage

class AdminMainView(TemplateView):
    template_name = 'adminapp/admin.html'

    def get_context_data(self, **kwargs):
        parent_context = super(AdminMainView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'Админка | Главная'
        parent_context['page_name'] = 'Админка сайта'
        return parent_context


class AdminOrdersView(TemplateView):
    template_name = 'adminapp/admin_orders.html'

    def get_context_data(self, **kwargs):
        parent_context = super(AdminOrdersView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'Админка | Заказы'
        parent_context['page_name'] = 'Заказы'
        return parent_context


class AdminProductsView(TemplateView):
    template_name = 'adminapp/admin_products.html'
    model = Product

    def get_context_data(self, **kwargs):
        parent_context = super(AdminProductsView, self).get_context_data(**kwargs)
        parent_context = {
            'page_title': 'Админка | Товары',
            'page_name': 'Товары',
            'product_objects': Product.objects.all(),
            'product_male_count': Product.objects.filter(gender='male').count(),
            'product_female_count': Product.objects.filter(gender='female').count(),
            'product_all_count': Product.objects.count(),
        }
        return parent_context


class AdminUsersView(TemplateView):
    template_name = 'adminapp/admin_users.html'

    def get_context_data(self, **kwargs):
        parent_context = super(AdminUsersView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'Админка | Юзеры'
        parent_context['page_name'] = 'Юзеры'
        return parent_context
