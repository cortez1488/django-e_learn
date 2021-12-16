from django.contrib import admin
from django.urls import path, include
from .views import Upload, Main

urlpatterns = [
    path('', Main.as_view(), name = "music_main"),
    path('upload/', Upload.as_view(), name = "music_upload"),
]
