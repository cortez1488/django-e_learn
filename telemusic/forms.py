from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(help_text='URI вашего видео...')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=75, required=False)
    file = forms.FileField()