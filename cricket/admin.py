from django.contrib import admin
from .models import CricketPosts,PostFuntions


@admin.register(CricketPosts)
class CricketPosts(admin.ModelAdmin):
    list_display = ('title','date')


@admin.register(PostFuntions)
class PostFuntions(admin.ModelAdmin):
    list_display = ('id','post_id','report')