"""educa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from .views import CreateUserView, StudentEnrollCourseView, StudentCoursesDetailView, StudentCoursesListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('registration/', CreateUserView.as_view(), name="registration"),
    path('enrolling/', StudentEnrollCourseView.as_view(), name='enrolling'),
    path('courses/', StudentCoursesListView.as_view(), name='student_course_list'),
    path('courses/<pk>/', StudentCoursesDetailView.as_view(), name='student_detail'),
    path('courses/<pk>/<module_id>/', StudentCoursesDetailView.as_view(), name='student_detail_module'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
