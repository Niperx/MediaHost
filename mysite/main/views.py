from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import TemplateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

from main.forms import NewUserForm, ProfileForm
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
    model = Profile
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        # username = None
        # if self.request.user.is_authenticated:
        #     username = self.request.user
        context = super().get_context_data(*args, **kwargs)
        username = self.kwargs.get("username")
        uid = None
        try:
            uid = User.objects.get(username=username)
        except:
            pass
        page_user = get_object_or_404(Profile, id=uid.id)
        context['page_user'] = page_user
        context['photos'] = Photo.objects.all().filter(created_by=uid).order_by("-created_at")
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


class EditProfilePageView(UpdateView):
    model = Profile
    template_name = 'edit_profile_page.html'
    form_class = ProfileForm
