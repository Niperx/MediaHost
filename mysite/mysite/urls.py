"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth.views import LoginView, LogoutView

from main.views import HomeView, RegisterView, ProfileView, CreateProfilePageView, \
    UploadPhoto, UploadVideo, AlbumView, CreateAlbum, AlbumViewAll

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='homepage'),

    path('profile/<username>', ProfileView.as_view(), name='profile'),
    path('profile/<username>/All', AlbumViewAll.as_view(), name='profile_album_all'),
    path('profile/<username>/<album>', AlbumView.as_view(), name='profile_album'),

    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),

    path('upload_photo/', UploadPhoto.as_view(), name='upload_photo'),
    path('upload_video/', UploadVideo.as_view(), name='upload_video'),
    path('create_album/', CreateAlbum.as_view(), name='create_album'),
    path('register', RegisterView.as_view(success_url='/'), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
