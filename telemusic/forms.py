from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(help_text='URI вашего видео...')

class UploadFileForm(forms.Form):
    file = forms.FileField()