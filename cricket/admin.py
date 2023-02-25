from django.contrib import admin
from .models import *

    
@admin.register(HostCricketTournaments)
class HostTournaments(admin.ModelAdmin):
    list_display = ('tournament_name','id','host')
    

@admin.register(Tournament_Notifications)
class HostTournaments(admin.ModelAdmin):
    list_display = ('tournament','verified','cancelled','reported')
    