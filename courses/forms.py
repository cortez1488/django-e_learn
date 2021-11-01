from django import forms
from django.forms.models import inlineformset_factory
from django import forms
from .models import Course, Module, RatingStar, Rating, Review

ModuleFormSet = inlineformset_factory(Course, Module, fields=['name','description'], extra=2, can_delete=True)

class SearchForm(forms.Form):
    search = forms.CharField(label='Поиск курсов', max_length=100, required=False)

class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(label = 'Оценить по-своему', queryset=RatingStar.objects.all(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'grade')

class SortForm(forms.Form):
    sort_choice = [
        ('STNDRT', 'Стандартная'),
    ('IPR', 'По возрастанию цены'),
    ('DPR', 'По убываению цены'),
        ('DT', 'Новинки'),
    ('IRT', 'Рейтинга у пользоваетелей'),
]
    sorting = forms.ChoiceField(label='Сортировка', choices=sort_choice)