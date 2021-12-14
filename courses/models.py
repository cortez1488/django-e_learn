from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .fields import OrderField
from autoslug import AutoSlugField
# Create your models here.
# Stars

class Tags(models.Model):
    name = models.CharField(max_length=25)
    course = models.ManyToManyField('Course', verbose_name='Курс')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Review(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(max_length=1500)
    date = models.DateField(auto_now_add=True)
    grade = models.BooleanField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='childs')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class RatingStar(models.Model):
    value = models.SmallIntegerField("Значение", default='0')

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ['-value']

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='фильм')

    def __str__(self):
        return f"{self.star}-{self.course}"
    class Meta:
        verbose_name='Рейтинг'
        verbose_name_plural = 'Рейтинги'

class Subject(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    students = models.ManyToManyField(User, blank=True, related_name='courses_students')
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owners', on_delete = models.SET_NULL, null=True)
    created = models.DateField(auto_now_add=True)
    overview = models.TextField()
    price = models.IntegerField('Цена', default=0)
    views_count = models.IntegerField("Просмотры курса", default=0)
    mean_rating = models.DecimalField('Рейтинг', default=0, decimal_places=2, max_digits=3)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return f'{self.name}. {self.price}'

class Module(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length = 200)

    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])


    def __str__(self):
        return f'{self.order}. {self.name}'

    class Meta:
        ordering = ['order']

class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='content')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':( 'text',\
                                                                                                           'video',\
                                                                                                           'image',\
                                                                                                           'file')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') # = itme
    order = OrderField(blank=True, for_fields = ['module'])  #????

    class Meta:
        ordering = ['order']


class BaseItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item':self})

    def __str__(self):
        return self.title
    class Meta:
        abstract = True

class Text(BaseItem):
    text = models.TextField()

class Image(BaseItem):
    image = models.ImageField(upload_to='videos')

class Video(BaseItem):
    video = models.URLField()

class File(BaseItem):
    file = models.FileField(upload_to='files')