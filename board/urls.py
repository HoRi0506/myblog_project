from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # 게시글 목록 페이지
    path('create/', views.post_create, name='post_create'),  # 게시글 작성 페이지
    path('<int:pk>/', views.post_detail, name='post_detail'),  # 게시글 상세 페이지
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),  # 게시글 수정
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),  # 게시글 삭제
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),  # 댓글
    path('<int:pk>/like/', views.post_like, name='post_like'),  # 좋아요 기능
]