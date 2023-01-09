from django.contrib import admin
from django.urls import path

from music_library import views

urlpatterns = [
    path('music_lib', views.MusicList.as_view())
]
