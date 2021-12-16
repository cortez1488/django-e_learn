from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from .service import handle_uploaded_file
from .forms import UploadFileForm

# Create your views here.

class Download(View):
    def get(self, request):pass

class Upload(View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse(status=201)

class Main(TemplateView):
    template_name = 'telemusic/index.html'