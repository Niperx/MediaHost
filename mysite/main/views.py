from django.views.generic import TemplateView, FormView


class HomeView(TemplateView):

    template_name = 'index.html'
