from django.views.generic import TemplateView


class BasketView(TemplateView):
    template_name = 'basket/basket.html'
