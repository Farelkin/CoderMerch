from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from products.models import Product, ProductImage, ProductCategory


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


class AdminProductsView(ListView):
    template_name = 'adminapp/admin_products.html'
    paginate_by = 10

    def get_context_data(self,  pk=None, **kwargs):
        parent_context = super(AdminProductsView, self).get_context_data(**kwargs)

        filter_male = Product.objects.filter(gender='male')
        filter_female = Product.objects.filter(gender='female')
        product_objects = Product.objects.all()
        q = self.request.GET.get("browse")

        parent_context = {
            'page_title': 'Админка | Товары',
            'page_name': 'Товары',
            'product_objects': product_objects,
            'product_male_count': filter_male,
            'product_female_count': filter_female,
            'input': q,
        }
        return parent_context

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

    # def get_queryset(self, **kwargs):
    #
    #     queryset = Product.objects.all()
    #
    #     if self.request.GET.get("browse"):
    #         selection = self.request.GET.get("browse")
    #         if selection == "male":
    #             queryset = Product.objects.filter(gender='male')
    #         elif selection == "female":
    #             queryset = Product.objects.filter(gender='female')
    #         else:
    #             queryset = Product.objects.all()
    #
    #     return queryset


def nav_filter_bar(request, pk):

    if pk == 1:
        nav_filter = Product.objects.filter(gender='female')
    elif pk == 2:
        nav_filter = Product.objects.filter(gender='male')

    context = {'product_objects': nav_filter}

    return render(request, 'adminapp/admin_products.html', context)


class AdminUsersView(TemplateView):
    template_name = 'adminapp/admin_users.html'

    def get_context_data(self, **kwargs):
        parent_context = super(AdminUsersView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'Админка | Юзеры'
        parent_context['page_name'] = 'Юзеры'
        return parent_context
