from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ModuleFormSet, SearchForm, RatingForm, ReviewForm, SortForm, FilterRatingForm, FilterPriceForm
from students.forms import CourseEnrollForm
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import redirect, get_object_or_404
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content, Course, Subject, Rating, Review, Tags
from django.http import HttpResponseRedirect, HttpResponse
from .correct_title import correct_name
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from statistics import mean
from django.core.serializers import serialize
import json
# Create your views here.


class UpdateReview(UpdateView):
    form_class = ReviewForm
    success_url = ''
    template_name = r'courses\reviews\review_updating.html'
    queryset = Review.objects.all()

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.success_url = reverse_lazy('course_detail', kwargs={'slug':self.get_object().course.slug})

class AddReview(View):
    def post(self, request):
        course = Course.objects.get(id=request.POST.get('course'))
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            print(request.POST)
            if request.POST.get('parent') != '':
                parent = Review.objects.get(id=int(request.POST.get('parent')))
                review.parent = parent
            review.user = request.user
            review.course = course
            review.save()
            return redirect("course_detail", slug=course.slug)
        else:
            return HttpResponse(status=400)

class AddStarRating(View):
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(id=request.POST.get('course'))
            Rating.objects.update_or_create(user=request.user, course = course,
                                                defaults = {'star':form.cleaned_data['star']})
            course.mean_rating = round((mean([i.star.value for i in course.rating_set.all()])), 2)
            course.save()
            return redirect("course_detail", slug=course.slug)
        else:
            return HttpResponse(status=400)

class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = r'courses\general\course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollform'] = CourseEnrollForm(initial={'course':self.object})
        context['rating_form'] = RatingForm
        context['views_counter'] = self.object.views_count
        context['review_form'] = ReviewForm
        context['reviews'] = self.object.review_set.all()
        context['mean_rating'] = self.object.mean_rating
        return context

    def get(self, request, *args, **kwargs):
        returned = super().get(request, *args, **kwargs)
        self.object.views_count += 1
        self.object.save()
        return returned

class CourseFiltering():

    def filtering(self, request):
        self.filter_by_price(request)
        self.filter_by_rating(request)

    def filter_by_price(self, request):
        if request.GET.get('pr_lte') != '':
            self.queryset = self.queryset.filter(price__lte=int(request.GET.get('pr_lte')))

        if request.GET.get('pr_gte') != '':
            self.queryset = self.queryset.filter(price__gte=int(request.GET.get('pr_gte')))

    def filter_by_rating(self, request):
        if request.GET.get('rating') != '':
            self.queryset = self.queryset.filter(mean_rating__gte=request.GET.get('rating'))


class CourseListSortingContextMixin(CourseFiltering):
    sort_dict = {'IPR':'price',
                'DPR':'-price',
                 'DT':'-created',
                 'IRT':'-mean_rating',}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all().annotate(num_courses=Count('courses'))
        context['course_counter'] = self.queryset.count()
        context['form'] = SearchForm(initial={'search':self.search_str})
        context['sort_form'] = SortForm(initial={'sorting':self.request.GET.get('sorting')})
        context['filter_star_form'] = FilterRatingForm(initial={'rating':self.request.GET.get('rating')})
        context['filter_price_form'] = FilterPriceForm(initial={'pr_lte':self.request.GET.get('pr_lte'), 'pr_gte':self.request.GET.get('pr_gte')})
        return context

    def main(self, request, *args, **kwargs):
        if request.GET != {}:
            self.searching(request, *args, **kwargs)
            self.sorting(request)
            self.filtering(request)
        self.by_subject(kwargs)
        self.number_annotation()

    def searching(self, request, *args, **kwargs):
            self.search_str = request.GET.get('search')
            tags = Tags.objects.filter(name__icontains=self.search_str)
            self.queryset = self.get_queryset().filter(Q(name__icontains =      self.search_str) | \
                                                       Q(overview__icontains =  self.search_str)| \
                                                       Q(tags__in =[tag.id for tag in tags]))
            self.extra_context.update({'search_string': self.search_str})


    def by_subject(self, kwargs):
        if 'subject' in kwargs:
            subject = get_object_or_404(Subject, slug=kwargs['subject'])
            self.queryset = self.get_queryset().filter(subject=subject)
            self.extra_context.update({'search_by_subject': subject.slug})

    def sorting(self, request):
            sorting = self.request.GET.get('sorting')
            if sorting != 'STNDRT':
                self.queryset = self.get_queryset().order_by(self.sort_dict[sorting])


    def number_annotation(self):
        self.queryset = self.get_queryset().annotate(num_modules=Count('modules'))


class CourseListSearchView(CourseListSortingContextMixin, ListView):
    model = Course
    template_name = r'courses\general\course_list_search.html'
    context_object_name = 'courses'

    def setup(self, request, *args, **kwargs):
        self.extra_context = {}
        self.search_str = ''
        super().setup(request, *args, **kwargs)
        self.main(request, *args, **kwargs)


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__owner=request.user).update(order=order)
        return self.render_json_response({'saved':'OK'})

class ModuleOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner = request.user).update(order=order)
        return self.render_json_response({'saved', 'OK'})

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        module_content = module.content.all()
        return self.render_to_response({'module':module, 'module_content':module_content})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.content_object.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'file', 'video', 'image']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])

        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance = self.obj)
        return self.render_to_response({'form':form, 'obj':self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST,  files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, content_object=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form':form, 'object':self.obj})


class CourseModuleUpdateView(TemplateResponseMixin,View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, id=kwargs['pk'], owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset=self.get_formset()
        return self.render_to_response({'course':self.course, 'formset':formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course, 'formset':formset})




class CourseList(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all()

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'name', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerEditMixin, OwnerCourseMixin):
    template_name = 'courses/manage/course/form.html'
    permission_required = 'courses_view_course'

class ManageCourseListView(OwnerCourseMixin, ListView):
    context_object_name = 'courses'
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

    def form_valid(self, form):

        """If the form is valid, save the associated model."""
        obj = form.save(commit=False)
        obj.slug=correct_name(form.cleaned_data['name'])
        obj.owner = self.request.user
        self.object = obj
        obj.save()

        """If the form is valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

def JsonListView(request):

    def normalLook(object):
        subject = Subject.objects.get(id = object.pop('subject'))
        owner = User.objects.get(id = object.pop('owner'))
        return (subject, owner, object)

    if request.method == 'GET':
        courses = Course.objects.order_by('pk').filter(pk__gt=request.GET['lastId'])[:1]
        content = serialize('json', courses)
        response = HttpResponse(content)
        return response
    elif request.method == 'POST':
        obj = normalLook(json.loads(request.body))
        print(obj)
        #course = Course.objects.create(subject = obj[0], owner = obj[1], **(obj[2]))
        #return HttpResponse(serialize('json', course))
        return HttpResponse('{"status":"ok"}')




def JSONTemplate(requset):
    courses = Course.objects.order_by('pk')[:1]
    return render(requset,  r'courses\general\index.html', {'coursesFst':courses})