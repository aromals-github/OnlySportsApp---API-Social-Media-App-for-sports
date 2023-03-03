from django.contrib import admin
from .models import *




@admin.register(MemberStatus)
class MemberStatusRegister(admin.ModelAdmin):
    list_display = ('club','member','status')
    
    
    
@admin.register(ClubCricketMembers)
class MemberStatusRegister(admin.ModelAdmin):
    list_display = ('club','tournament',)
    
    
    
@admin.register(ClubFootballMembers)
class MemberStatusRegister(admin.ModelAdmin):
    list_display = ('club','tournament',)
    
    
@admin.register(MemberTournamentStatus)
class MemberStatusRegister(admin.ModelAdmin):
    list_display = ('club','member','status')
    
    
@admin.register(ClubRegisteredCricketTournament)
class MemberStatusRegister(admin.ModelAdmin):
    list_display = ('club',)
    
@admin.register(ClubRegisteredFootballTournament)
class MemberStatusRegister(admin.ModelAdmin):
    list_display = ('club',)
    
    
@admin.register(Club_Games_History)
class MemberStatusRegister(admin.ModelAdmin):
    list_display = ('club','registered_cricket','registered_football','cricket_won','football_won')