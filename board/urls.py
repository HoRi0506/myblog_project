from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # 게시글 목록 페이지
    path('create/', views.post_create, name='post_create'),  # 게시글 작성 페이지
]