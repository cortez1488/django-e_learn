from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import BaseFormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from courses.models import Course
# Create your views here.

class CreateUserView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("course_list_all")
    template_name = "students/student/users_create.html"

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result

class StudentEnrollCourseView(BaseFormView, LoginRequiredMixin):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('student_detail',
                            args=[self.course.id])


class StudentCoursesListView(ListView):
    template_name = "students/course/list.html"

    def get_queryset(self):
        return Course.objects.filter(students__in=[self.request.user])

class StudentCoursesDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        return Course.objects.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object #get_object
        print(course.name)
        if 'module_id' in self.kwargs:
            module = course.modules.get(id = self.kwargs['module_id'])
            context['module'] = module
        else:
            module = course.modules.first()
            context['module'] = module
        context['module_context'] = module.content.all()
        return context