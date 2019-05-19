from django.views.generic import TemplateView


class BasketView(TemplateView):
    template_name = 'basket/basket.html'


class OrderDoneView(TemplateView):
    template_name = 'basket/basket_user_order.html'
