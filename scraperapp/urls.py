from django.urls import path

from . import views

app_name='scraperapp'

urlpatterns = [
    path('', views.index),
]
