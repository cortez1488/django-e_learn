from django.conf import settings

def handle_uploaded_file(f):
    with open(settings.MUSIC_STORAGE_PATH+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)