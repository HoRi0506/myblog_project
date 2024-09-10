from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=255)  # Repository 이름
    description = models.TextField(blank=True)  # Repository 설명
    created_at = models.DateTimeField()  # Repository 생성 일시
    last_push_at = models.DateTimeField()  # 마지막으로 push된 일시
    github_url = models.URLField(max_length=255)  # GitHub repository URL
    image = models.ImageField(upload_to='git_post/', blank=True, null=True, default='git_post/git_image.png')  # 기본 이미지 설정

    def __str__(self):
        return self.name

    # 최근 7일 이내에 push된 repository는 "update" 표시
    def is_updated(self):
        import datetime
        return (datetime.datetime.now() - self.last_push_at).days <= 7

    # 최근 생성된 repository는 "new" 표시
    def is_new(self):
        import datetime
        return (datetime.datetime.now() - self.created_at).days <= 7
