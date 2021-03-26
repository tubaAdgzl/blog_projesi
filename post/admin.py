from django.contrib import admin
from .models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title","author","date"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name","content","created_date"]