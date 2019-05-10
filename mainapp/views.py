from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'mainapp/index.html'


class AboutView(TemplateView):
    template_name = 'mainapp/about.html'


