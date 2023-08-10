from django.urls import path
from . import views

urlpatterns = [
    path('get-subjects', views.getSubjects),
    path('subject-courses/<str:subject_code>', views.getSubjectCourses),
    path('search-courses/<str:keyword>', views.searchCourses),
    path('get-course/<str:keyword>', views.getCourse),
    path('prerequisite-details/<str:course_code>', views.getCoursePrerequisites),
]
