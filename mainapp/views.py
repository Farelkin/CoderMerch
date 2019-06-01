from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        parent_context = super(HomeView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'CoderMerch | Главная'
        return parent_context


class AboutView(TemplateView):
    template_name = 'mainapp/about.html'

    def get_context_data(self, **kwargs):
        parent_context = super(AboutView, self).get_context_data(**kwargs)
        parent_context['page_title'] = 'CoderMerch | О команде'
        return parent_context


class AccountView(TemplateView):
    template_name = 'mainapp/account.html'
