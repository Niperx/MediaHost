from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from django.views.generic import TemplateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User

from main.forms import NewUserForm, ProfileForm, ImageForm
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
        uid = get_object_or_404(User, username=username)
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


class CreateProfilePageView(CreateView):
    model = Profile

    template_name = 'create_profile.html'
    fields = ['profile_pic', 'bio', 'facebook', 'twitter', 'instagram']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('profile')


def upload_photo(request):
    submitted = False
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.created_by = request.user.id
            img.save()
            return redirect('homepage')

    form = ImageForm()
    return render(request, 'upload_photo.html', {'form' : form})

class UploadPhoto(CreateView):
    model = Photo
    template_name = 'upload_photo.html'
    form_class = ImageForm

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.created_by = self.request.user.id
        photo.save()
        return super().form_valid(form)

    success_url = '/'