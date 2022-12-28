from django.contrib import admin
from .models import FootballPosts,PostFuntions


@admin.register(FootballPosts)
class FootballPosts(admin.ModelAdmin):
    list_display = ('title','date','id','user')


@admin.register(PostFuntions)
class PostFuntions(admin.ModelAdmin):
    list_display = ('id','post_id','report')
