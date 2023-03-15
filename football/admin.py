from django.contrib import admin
from .models import *

    
@admin.register(HostFootballTournaments)
class HostTournaments(admin.ModelAdmin):
    list_display = ('tournament_name','id','host')
    

@admin.register(Tournament_Notifications)
class HostTournaments(admin.ModelAdmin):
    list_display = ('tournament','verified','cancelled','reported')


@admin.register(Tournament_Reports)
class Reports(admin.ModelAdmin):
    list_display = ('tournament','count_reporters')



@admin.register(Resgister_Tournaments)
class Reports(admin.ModelAdmin):
    list_display = ('tournament','count_teams')
    
    
    

@admin.register(Participants)
class Participants_Football(admin.ModelAdmin):
    list_display = ('tournament','count_participants')
    
    

@admin.register(FootballTournamentResult)
class Results_Football(admin.ModelAdmin):
    list_display = ('tournament','won')