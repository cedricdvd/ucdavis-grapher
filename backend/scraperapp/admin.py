from django.contrib import admin
from .models import Subject, Course, Prerequisite

# Register your models here.
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Prerequisite)
