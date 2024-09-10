from django.contrib import admin
from .models import Repository

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'last_push_at', 'github_url')
    search_fields = ['name', 'description']