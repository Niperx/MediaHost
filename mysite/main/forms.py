from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm

from .models import Profile, Photo, Video, Album


class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']


class ImageForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'image')


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('caption', 'video')


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('title', )
