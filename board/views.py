from django.shortcuts import render, redirect
from .models import Post  # 게시글 모델
from django.contrib.auth.decorators import login_required
from .forms import PostForm  # 게시글 작성 폼
from django.core.paginator import Paginator
import logging

# 로그 설정
logger = logging.getLogger(__name__)

# 로그인한 사용자만 게시글 작성 가능
@login_required
def post_create(request):
    try:
        if request.method == 'POST':  # POST 요청이면, 폼 데이터를 받아 처리
            form = PostForm(request.POST)  # 작성된 데이터로 폼 생성
            if form.is_valid():  # 폼 유효성 검사
                post = form.save(commit=False)  # 작성자 추가 전 대기
                post.author = request.user  # 현재 로그인된 사용자를 작성자로 추가
                post.save()  # 게시글 저장
                logger.info(f"New post created by {request.user}: {post.title}")
                return redirect('post_list')  # 게시글 목록 페이지로 리디렉트
            else:
                logger.error(f"Form validation error: {form.errors}")
        else:
            form = PostForm()  # GET 요청 시 빈 폼 생성
            logger.info(f"New post form displayed for {request.user}")
    except Exception as e:
        logger.error(f"Error in post_create: {str(e)}")
        form = PostForm()  # 오류 발생 시 폼 다시 생성

    return render(request, 'board/post_create.html', {'form': form})  # 템플릿에 폼 전달

# 게시글 목록을 출력하는 뷰 함수
def post_list(request):
    try:
        query = request.GET.get('q')  # 검색어 가져오기
        if query:
            posts = Post.objects.filter(title__icontains=query).order_by('-created_at')  # 검색어가 포함된 게시글을 최신 순으로 정렬
            logger.info(f"Search performed with query: {query}")
        else:
            posts = Post.objects.all().order_by('-created_at')  # 모든 게시글을 최신 순으로 정렬
            logger.info("Post list requested without search query")

        # 페이지네이션 처리 (한 페이지에 10개의 게시글 표시)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'board/post_list.html', {
            'posts': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
        })
    except Exception as e:
        logger.error(f"Error in post_list: {str(e)}")
        return render(request, 'board/post_list.html', {'posts': []})