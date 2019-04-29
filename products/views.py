from django.views.generic import TemplateView


class ProductsView(TemplateView):
    template_name = 'products/products.html'


class ProductView(TemplateView):
    template_name = 'products/product.html'
