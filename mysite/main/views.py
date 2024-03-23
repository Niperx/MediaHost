from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from django.views.generic import TemplateView, FormView, UpdateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User

from main.forms import NewUserForm, ProfileForm, ImageForm, VideoForm, AlbumForm
from main.models import Photo, Profile, Video, Album


class HomeView(TemplateView):

    template_name = 'index.html'


class RegisterView(FormView):

    template_name = 'register.html'
    form_class = NewUserForm

    def form_valid(self, form):
        form.save()
        return redirect('login')


# class ProfileView(TemplateView):
#     model = Profile
#     template_name = 'profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         username = self.kwargs.get("username")
#         uid = get_object_or_404(User, username=username)
#         page_user = get_object_or_404(Profile, id=uid.id)
#         context['page_user'] = page_user
#         context['photos'] = Photo.objects.all().filter(created_by=uid).order_by("-created_at")
#         context['videos'] = Video.objects.all().filter(created_by=uid).order_by("-created_at")
#         return context


class ProfileView(TemplateView):
    model = User
    template_name = 'profile_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        uid = get_object_or_404(User, username=username)
        # page_user = get_object_or_404(Profile, id=uid.id)
        context['page_user'] = uid
        context['albums'] = Album.objects.all().filter(created_by=uid).order_by("-created_at")
        # context['photos'] = Photo.objects.all().filter(created_by=uid).order_by("-created_at")
        # context['videos'] = Video.objects.all().filter(created_by=uid).order_by("-created_at")
        return context


class AlbumView(TemplateView):

    template_name = 'profile_album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        album_title = self.kwargs.get("album")
        uid = get_object_or_404(User, username=username)
        album = get_object_or_404(Album, title=album_title)
        # page_user = get_object_or_404(Profile, id=uid.id)
        context['can_delete'] = True
        context['album'] = Album.objects.all().filter(title=album_title)[0]
        context['page_user'] = uid
        context['photos'] = Photo.objects.all().filter(created_by=uid, album=album).order_by("-created_at")
        context['videos'] = Video.objects.all().filter(created_by=uid, album=album).order_by("-created_at")
        return context


class AlbumViewAll(TemplateView):

    template_name = 'profile_album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        uid = get_object_or_404(User, username=username)
        # page_user = get_object_or_404(Profile, id=uid.id)
        context['can_delete'] = False
        context['page_user'] = uid
        context['photos'] = Photo.objects.all().filter(created_by=uid, album=None).order_by("-created_at")
        context['videos'] = Video.objects.all().filter(created_by=uid, album=None).order_by("-created_at")
        return context


class LargePhoto(TemplateView):

    template_name = 'image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        print(pk)
        img = get_object_or_404(Photo, pk=pk)
        # print(img.url)
        context['image'] = img
        return context


class CreateProfilePageView(CreateView):
    model = Profile

    template_name = 'create_profile.html'
    fields = ['profile_pic', 'bio']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('homepage')


class UploadPhoto(CreateView):
    model = Photo
    template_name = 'upload_photo.html'
    form_class = ImageForm()

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.created_by = self.request.user
        photo.save()
        return super().form_valid(form)

        # return redirect(f'profile/{self.request.user.username}')

    success_url = reverse_lazy('homepage')


def upload_photo(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.created_by = request.user
            photo.save()
        return redirect('homepage')

    form = ImageForm(user=request.user)
    return render(request, 'upload_photo.html', {'form': form})


class UploadVideo(CreateView):
    model = Video
    template_name = 'upload_video.html'
    form_class = VideoForm

    def form_valid(self, form):
        video = form.save(commit=False)
        video.created_by = self.request.user
        video.save()
        return super().form_valid(form)

    success_url = reverse_lazy('homepage')


class CreateAlbum(CreateView):
    model = Album
    template_name = 'create_album.html'
    form_class = AlbumForm

    def form_valid(self, form):
        video = form.save(commit=False)
        video.created_by = self.request.user
        video.save()
        return super().form_valid(form)

    success_url = reverse_lazy('homepage')


def delete_album(request, pk):

    if not request.user.is_authenticated:
        return redirect('homepage')

    al = Album.objects.get(pk=pk)
    al.delete()

    return redirect('homepage')


def delete_photo(request, pk):

    if not request.user.is_authenticated:
        return redirect('homepage')

    ph = Photo.objects.get(pk=pk)
    ph.delete()

    return redirect('homepage')

















# def upload_photo(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         return redirect('homepage')
#
#     form = ImageForm()
#     return render(request, 'upload_photo.html', {'form': form})
