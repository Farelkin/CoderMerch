from django.views.generic import TemplateView
from basket.models import Basket


class BasketView(TemplateView):
    template_name = 'basket/basket.html'

    def get_context_data(self, **kwargs):
        parent_context = super(BasketView, self).get_context_data(**kwargs)
        parent_context['basket'] = Basket.objects.filter(user=self.request.user, is_ordered=False)
        return parent_context


class OrderDoneView(TemplateView):
    template_name = 'basket/basket_user_order.html'
