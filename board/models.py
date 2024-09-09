from django.db import models
from django.contrib.auth.models import User

# 게시글 목록
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 게시글 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 게시글 수정 시간
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # 좋아요한 사용자들

    def total_likes(self):
        return self.likes.count()  # 좋아요 수 반환
    
    def __str__(self):
        return self.title

# 댓글
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # 댓글이 달린 게시글
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 댓글 작성자
    text = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간

    def __str__(self):
        return f'{self.author} - {self.text[:20]}'  # 댓글 작성자와 댓글 내용 일부를 반환