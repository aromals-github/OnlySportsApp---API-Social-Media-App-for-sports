from django.contrib import admin
from .models import *



@admin.register(Clubs)
class Clubs(admin.ModelAdmin):
    list_display = ('name','district','id','owner')
    
    
@admin.register(ClubAdmins)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('club_name','owner')