from django.urls import path
from . import views

urlpatterns = [
    path('', views.git_post, name='git_post'),
]