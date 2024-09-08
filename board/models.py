from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 게시글 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 게시글 수정 시간
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title