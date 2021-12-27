from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, FileResponse
from .service import handle_uploaded_file, normal_name_for_download
from .forms import UploadFileForm
from .models import Music

# Create your views here.

class Download(View):
    def get(self, request):
        response = FileResponse(open(request.GET['path'], 'rb'))
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(normal_name_for_download(request.GET['name'])) #Имена файлов не должны быть на русском
        return response

class Upload(View):
    def post(self, request):
        print(request.FILES)
        if request.FILES != []:
             handle_uploaded_file(request.FILES['music'])
             return HttpResponse(status=201)
        return HttpResponse(status=400)

class Main(TemplateView):
    template_name = 'telemusic/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset'] = Music.objects.all()
        context['upload_form'] = UploadFileForm
        return context



