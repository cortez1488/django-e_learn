from django.contrib import admin
from .models import Subject, Course, Module

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