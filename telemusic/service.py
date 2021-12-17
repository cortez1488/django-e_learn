from django.conf import settings
from .models import Music
def handle_uploaded_file(f):
    Music.objects.create(path=settings.MUSIC_STORAGE_PATH+f.name, name=f.name)
    with open(settings.MUSIC_STORAGE_PATH+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)