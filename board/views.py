from django.shortcuts import render, redirect
from .models import Post  # 게시글 모델을 가져옴
from django.contrib.auth.decorators import login_required  # 로그인한 사용자만 작성 가능하도록 데코레이터 사용
from .forms import PostForm  # 게시글 작성 폼을 사용

# 게시글 목록을 출력하는 뷰 함수
def post_list(request):
    posts = Post.objects.all()  # 모든 게시글을 가져옴
    return render(request, 'board/post_list.html', {'posts': posts})

@login_required  # 로그인한 사용자만 접근 가능
def post_create(request):
    if request.method == 'POST':  # POST 요청이면, 폼 데이터를 받아 처리
        form = PostForm(request.POST)  # 작성된 데이터로 폼 생성
        if form.is_valid():  # 폼 유효성 검사
            post = form.save(commit=False)  # 데이터베이스에 저장하기 전 작성자 추가
            post.author = request.user  # 현재 로그인된 사용자를 게시글 작성자로 설정
            post.save()  # 데이터베이스에 게시글 저장
            return redirect('post_list')  # 저장 후 게시글 목록 페이지로 리다이렉트
    else:
        form = PostForm()  # GET 요청이면 빈 폼을 생성
    return render(request, 'board/post_create.html', {'form': form})  # 폼을 템플릿에 전달하여 렌더링