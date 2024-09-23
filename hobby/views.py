from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment  # 게시글 모델
from django.contrib.auth.decorators import login_required
from .forms import PostForm  # 게시글 작성 폼
from django.core.paginator import Paginator
from django.http import JsonResponse
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
                return redirect('hobby_post_list')  # 게시글 목록 페이지로 리디렉트
            else:
                logger.error(f"Form validation error: {form.errors}")
        else:
            form = PostForm()  # GET 요청 시 빈 폼 생성
            logger.info(f"New post form displayed for {request.user}")
    except Exception as e:
        logger.error(f"Error in post_create: {str(e)}")
        form = PostForm()  # 오류 발생 시 폼 다시 생성

    return render(request, 'hobby/post_create.html', {'form': form})  # 템플릿에 폼 전달

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

        return render(request, 'hobby/post_list.html', {
            'posts': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
        })
    except Exception as e:
        logger.error(f"Error in post_list: {str(e)}")
        return render(request, 'hobby/post_list.html', {'posts': []})

# 게시글 상세 페이지 보기
def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)  # 해당 게시글이 없으면 404 에러 반환
        
        # 조회수 증가(같은 사용자가 여러 번 접속해도 증가)
        post.counting += 1
        post.save()
        
        return render(request, 'hobby/post_detail.html', {'post': post})
    except Exception as e:
        logger.error(f"Error in post_detail: {str(e)}")
        return redirect('hobby_post_list')

# 게시글 수정
@login_required
def post_edit(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)

        if request.user != post.author and not request.user.is_superuser:
            logger.error(f"Unauthorized attempt to edit post {post.pk} by {request.user}")
            return redirect('hobby_post_list')  # 작성자나 관리자가 아니면 목록으로 리디렉션
        
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                logger.info(f"Post {post.pk} edited by {request.user}")
                return redirect('hobby_post_detail', pk=post.pk)  # 수정 후 상세 페이지로 리디렉션
            else:
                logger.error(f"Form validation error while editing post {post.pk}: {form.errors}")
        else:
            form = PostForm(instance=post)

        return render(request, 'hobby/post_edit.html', {'form': form, 'post': post})
    except Exception as e:
        logger.error(f"Error in post_edit: {str(e)}")
        return redirect('hobby_post_list')

# 게시글 삭제
@login_required
def post_delete(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        
        if request.user != post.author and not request.user.is_superuser:
            logger.error(f"Unauthorized attempt to delete post {post.pk} by {request.user}")
            return redirect('hobby_post_list')  # 작성자나 관리자가 아니면 목록으로 리디렉션

        if request.method == 'POST':
            post.delete()
            logger.info(f"Post {post.pk} deleted by {request.user}")
            return redirect('hobby_post_list')  # 삭제 후 목록으로 리디렉션

        return render(request, 'hobby/post_confirm_delete.html', {'post': post})
    except Exception as e:
        logger.error(f"Error in post_delete: {str(e)}")
        return redirect('hobby_post_list')

@login_required
def add_comment(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)  # 해당 게시글 가져오기
        if request.method == 'POST':
            comment_text = request.POST.get('comment')  # 폼에서 댓글 내용 가져오기
            if comment_text:
                comment = Comment.objects.create(
                    post=post,  # 댓글이 달린 게시글
                    author=request.user,  # 댓글 작성자
                    text=comment_text  # 댓글 내용
                )
                logger.info(f"New comment added by {request.user}: {comment.text}")
                return redirect('hobby_post_detail', pk=post.pk)  # 댓글 추가 후 게시글 상세보기로 리디렉트
            else:
                logger.error("No comment text provided")
        else:
            logger.error("Invalid request method for add_comment")
    except Exception as e:
        logger.error(f"Error in add_comment: {str(e)}")
    
    return redirect('hobby_post_detail', pk=post.pk)

@login_required
def post_like(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # 이미 좋아요를 눌렀으면 취소
            liked = False
        else:
            post.likes.add(request.user)  # 좋아요 추가
            liked = True

        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)