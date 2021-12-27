from django.conf import settings
from .models import Music
import transliterate

def handle_uploaded_file(f):
    if Music.objects.get_or_create(path=settings.MUSIC_STORAGE_PATH+f.name, name=f.name)[1]:
        with open(settings.MUSIC_STORAGE_PATH+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            return True
    else: return False

def normal_name_for_download(text):
    return transliterate.translit(text, 'uk', reversed=True)

