from django.contrib import admin
from django.urls import path, include
from .views import Upload, Main, Download

urlpatterns = [
    path('', Main.as_view(), name = "music_main"),
    path('upload/', Upload.as_view(), name = "music_upload"),
    path('download/', Download.as_view(), name = "music_download"),
]
