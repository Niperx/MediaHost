from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView

from main.forms import NewUserForm
from main.models import Photo, Profile


class HomeView(TemplateView):

    template_name = 'index.html'

    # def get_context_data(self, **kwargs):
    #     username = None
    #     if self.request.user.is_authenticated:
    #         username = self.request.user
    #     context = super().get_context_data(**kwargs)
    #     context['photos'] = Photo.objects.all().filter(created_by=username).order_by("-created_at")
    #     return context


class RegisterView(FormView):

    template_name = 'register.html'
    form_class = NewUserForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileView(TemplateView):

    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        username = None
        if self.request.user.is_authenticated:
            username = self.request.user
        context = super().get_context_data(**kwargs)
        # username = self.kwargs.get("username")
        # print(self.kwargs.get("username"))
        print(username)
        context['photos'] = Photo.objects.all().filter(created_by=username).order_by("-created_at")
        return context


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs.get("pk"))
        context['page_user'] = page_user
        return context
