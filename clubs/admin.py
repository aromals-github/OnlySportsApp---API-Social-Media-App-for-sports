from django.contrib import admin
from .models import *



@admin.register(Clubs)
class Clubs(admin.ModelAdmin):
    list_display        = ('name','district','id','owner')
    search_fields       = ('name','district')
    list_filter         = ('district',)
    fieldsets           = ()
@admin.register(MembershipRequest)
class ClubMembershipRequest(admin.ModelAdmin):
    list_display        = ('name','owner','sender')
    search_fields       = ('sender','')
   
    
@admin.register(ClubAdmins)
class ClubAdmin(admin.ModelAdmin):
    list_display        = ('club_name','owner','admin_count')
    search_fields       = ('club_name',)
    fieldsets           = ()


@admin.register(MembershipResponses)
class ClubMembershipList(admin.ModelAdmin):
    list_display        = ('club',)
    search_fields       = ('club',)
    list_filter         = ('club',)
    fieldsets           = ()
    
@admin.register(ClubHistoryPerUser)
class HistoryClub(admin.ModelAdmin):
    list_display        = ('user','owner')
    search_fields       = ('user',)
    fieldsets           = ()
