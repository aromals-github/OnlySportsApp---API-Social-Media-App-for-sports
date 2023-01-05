from django.contrib import admin
from .models import CricketPosts,PostFuntions,HostCricketTournaments,CricketClubs


@admin.register(CricketPosts)
class CricketPosts(admin.ModelAdmin):
    list_display = ('title','date','id','user')


@admin.register(PostFuntions)
class PostFuntions(admin.ModelAdmin):
    list_display = ('id','post_id','report','number_of_likes','number_of_dislikes')
    
    
@admin.register(HostCricketTournaments)
class HostTournaments(admin.ModelAdmin):
    list_display = ('id','tournament_name')
    
@admin.register(CricketClubs)
class Clubs(admin.ModelAdmin):
    list_display = ('name',)