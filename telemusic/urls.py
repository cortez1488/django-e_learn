from django.contrib import admin
from django.urls import path, include
from .views import Upload

urlpatterns = [
    path('upload/', Upload.as_view(), name = "music_upload"),
]
