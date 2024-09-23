from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='hobby_post_list'),  # hobby 게시판 목록
    path('create/', views.post_create, name='hobby_post_create'),  # 게시글 작성
    path('<int:pk>/', views.post_detail, name='hobby_post_detail'),  # 게시글 상세 페이지
    path('<int:pk>/edit/', views.post_edit, name='hobby_post_edit'),  # 게시글 수정
    path('<int:pk>/delete/', views.post_delete, name='hobby_post_delete'),  # 게시글 삭제
    path('<int:pk>/add_comment/', views.add_comment, name='hobby_add_comment'),  # 댓글
    path('<int:pk>/like/', views.post_like, name='hobby_post_like'),  # 좋아요 기능
]