from django.contrib import admin
from .models import Post, Topic, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'publish']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created']