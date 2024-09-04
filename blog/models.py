from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)  # 게시글 제목
    content = models.TextField()  # 게시글 내용
    created_at = models.DateTimeField(default=timezone.now)  # 작성 시간

    def __str__(self):
        return self.title  # 게시글 제목을 문자열로 반환