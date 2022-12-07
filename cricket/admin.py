from django.contrib import admin
from .models import CricketPosts


@admin.register(CricketPosts)
class CricketPosts(admin.ModelAdmin):
    list_display = ('title',)
