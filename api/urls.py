from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('subject-details/<str:subj>', views.subjectDetail),
    path('subject-courses/<str:subj>', views.subjectCourses),
    path('course-details/<str:course_code>', views.courseDetails),
    path('prerequisite-details/<str:course_code>', views.prerequisiteDetails)
]
