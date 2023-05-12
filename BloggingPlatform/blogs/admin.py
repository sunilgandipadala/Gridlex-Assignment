from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BlogPost, Comment#, UserProfile
from .models import *

# Register your models here.

admin.site.register(User, UserAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'description', 'body_text')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'blog_post', 'created_at')
    list_filter = ('blog_post', 'created_at')
    search_fields = ('user_name', 'email', 'comment_text')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name')

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
#admin.site.register(UserProfile, UserProfileAdmin)
