from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # 게시글 모델을 사용
        fields = ['title', 'content']  # 작성할 수 있는 필드는 제목과 내용