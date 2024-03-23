from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, ModelChoiceField

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
        fields = ('title', 'image', 'album')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['album'].queryset = Album.objects.filter(created_by=user)
            self.fields['album'].required = False


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('caption', 'video', 'album')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['album'].queryset = Album.objects.filter(created_by=user)
            self.fields['album'].required = False


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'is_private')

