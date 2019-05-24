
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from products.models import Product, ProductImage, ProductCategory
from .filters import AdminProductFilter



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
    template_name = 'adminapp/somefilter.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all'] = Product.objects.all()
        context['filter'] = AdminProductFilter(self.request.GET, queryset=self.get_queryset())
        return context

# class AdminProductsView(ListView):
#     template_name = 'adminapp/admin_products.html'
#     paginate_by = 5
#     model = Product
#
#     def get_queryset(self):
#         filter_val = self.request.GET.get('male')
#         new_context = Product.objects.filter(gender=filter_val,)
#         return new_context
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(AdminProductsView, self).get_context_data(**kwargs)
#         context['gender'] = self.request.GET.get('male')
#         return context

    # def get_context_data(self,  pk=None, **kwargs):
    #     parent_context = super(AdminProductsView, self).get_context_data(**kwargs)
    #
    #     filter_male = Product.objects.filter(gender='male')
    #     filter_female = Product.objects.filter(gender='female')
    #     product_objects = Product.objects.all()
    #
    #     parent_context = {
    #         'page_title': 'Админка | Товары',
    #         'page_name': 'Товары',
    #         'product_objects': product_objects,
    #         'product_male_count': filter_male,
    #         'product_female_count': filter_female,
    #     }
    #     return parent_context

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     return queryset

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

    if pk == 'all':
        nav_filter = Product.objects.all()
    elif pk == 'male':
        nav_filter = Product.objects.filter(gender='male')
    elif pk == 'female':
        nav_filter = Product.objects.filter(gender='female')
    elif pk == '1':  # 1 - толстовка 2 - жакет  3 - рубашка  4 - свитер  5 - футболка
        nav_filter = Product.objects.filter(category='1')
    elif pk == '2':
        nav_filter = Product.objects.filter(category='2')
    elif pk == '3':
        nav_filter = Product.objects.filter(category='3')
    elif pk == '4':
        nav_filter = Product.objects.filter(category='4')
    elif pk == '5':
        nav_filter = Product.objects.filter(category='5')

    context = {
                'page_title': 'Админка | Товары',
                'page_name': 'Товары',
                'product_objects': nav_filter,
                'product_female_count': Product.objects.filter(gender='female'),
                'product_male_count': Product.objects.filter(gender='male'),
               }

    return render(request, 'adminapp/admin_products.html', context)



class AdminUsersView(TemplateView):
    template_name = 'adminapp/admin_users.html'

    def get_context_data(self, **kwargs):
        parent_context = super(AdminUsersView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'Админка | Юзеры'
        parent_context['page_name'] = 'Юзеры'
        return parent_context
