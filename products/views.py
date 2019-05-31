from django.views.generic import TemplateView


class ManProductsView(TemplateView):
    template_name = 'products/man.html'


class WomanProductsView(TemplateView):
    template_name = 'products/woman.html'


class ProductView(TemplateView):
    template_name = 'products/product.html'


class LikeView(TemplateView):
    template_name = 'products/like.html'
