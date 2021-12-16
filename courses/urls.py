from django.contrib import admin
from django.urls import path, include
from .views import ManageCourseListView, CourseCreateView, CourseUpdateView, \
CourseDeleteView, CourseModuleUpdateView, ContentCreateUpdateView, ContentDeleteView, \
ModuleContentListView, ModuleOrderView, ContentOrderView, CourseDetailView, \
CourseListSearchView, AddStarRating, AddReview, UpdateReview, JsonListView, JSONTemplate

urlpatterns = [
    path('', CourseListSearchView.as_view() ,name = "course_list_all"),
    path('json/', JsonListView, name="json_testing"),
    path('testing/', JSONTemplate, name="testing"),
    path('add-rating/', AddStarRating.as_view() ,name = "course_add_rating"),
    path('add-review/', AddReview.as_view() ,name = "course_add_review"),
    path('detail/<slug:slug>/', CourseDetailView.as_view() ,name = "course_detail"),
    path('mine/', ManageCourseListView.as_view() ,name = "manage_course_list"),
    path('create/', CourseCreateView.as_view() ,name = "course_create"),
    path('<pk>/edit/', CourseUpdateView.as_view() ,name = "course_edit"),
    path('<pk>/delete/', CourseDeleteView.as_view() ,name = "course_delete"),
    path('<pk>/module/', CourseModuleUpdateView.as_view() ,name = "course_module_update"),

    path('module/order/', ModuleOrderView.as_view(), name = "module_order"),
    path('content/order/', ContentOrderView.as_view(), name = "content_order"),
    path('module/<int:module_id>/', ModuleContentListView.as_view(), name = "module_content_list"),
    path('module/<int:module_id>/content/<model_name>/create/', ContentCreateUpdateView.as_view() ,name = "module_content_create"),
    path('module/<int:module_id>/content/<model_name>/', ContentCreateUpdateView.as_view() ,name = "module_content_update"),
    path('content/<int:id>/delete/', ContentDeleteView.as_view(), name = 'module_content_delete'),
    path('search/', CourseListSearchView.as_view() ,name = "course_list_search"),
    path('<slug:subject>/', CourseListSearchView.as_view() ,name = "course_list_by_subject"),

    path('review/<int:pk>', UpdateReview.as_view() ,name = "review_update"),

]