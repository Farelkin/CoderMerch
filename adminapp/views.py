from django.views.generic import TemplateView


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

    def get_context_data(self, **kwargs):
        parent_context = super(AdminProductsView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'Админка | Товары'
        parent_context['page_name'] = 'Товары'
        return parent_context


class AdminUsersView(TemplateView):
    template_name = 'adminapp/admin_users.html'

    def get_context_data(self, **kwargs):
        parent_context = super(AdminUsersView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'Админка | Юзеры'
        parent_context['page_name'] = 'Юзеры'
        return parent_context
