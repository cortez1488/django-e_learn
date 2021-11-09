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
        widgets = {
            'star' :forms.Select(attrs={'class':'form-control'}),
        }

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

class FilterRatingForm(forms.Form):
    rate_choice = [
        ('', ''),
        ('4.5', '4.5 звезды'),
        ('4', '4 звезды'),
        ('3.5', '3.5 звезды'),
        ('3', '3 звезды'),]

    rating = forms.ChoiceField(label='Рейтинг', choices=rate_choice, widget=forms.Select, required=False,)

class FilterPriceForm(forms.Form):
    pr_lte = forms.IntegerField(label='Цена до', required=False)
    pr_gte = forms.IntegerField(label='Цена от', required=False)