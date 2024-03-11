from django.views.generic import TemplateView, FormView

from main.forms import NewUserForm
from main.models import Photo


class HomeView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        username = None
        if self.request.user.is_authenticated:
            username = self.request.user
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.all().filter(created_by=username).order_by("-created_at")
        return context


class RegisterView(FormView):

    template_name = 'register.html'
    form_class = NewUserForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)