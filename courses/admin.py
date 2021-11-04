from django.contrib import admin
from .models import Subject, Course, Module, Tags, Review, Rating

@admin.register(Subject)
class AdminSubject(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

class ModuleInline(admin.StackedInline):
    model = Module
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ['name', 'subject', 'owner', 'created']
    list_filter = ['subject', 'owner']
    search_fields = ['owner', 'name', 'subject']
    prepopulated_fields = {'slug':('name',)}
    inlines = [ModuleInline]


@admin.register(Tags)
class AdminTags(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ['name']
    search_fields = ['name']

@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ['course', 'user', 'grade']
    list_filter = ['date']
    search_fields = ['name', 'course', 'text', 'user']

@admin.register(Rating)
class AdminRating(admin.ModelAdmin):
    list_display = ['course', 'star', 'user' ]
    list_filter = ['course', ]
    search_fields = ['course']


