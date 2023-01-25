from django.contrib import admin
from .models import Clubs



@admin.register(Clubs)
class Clubs(admin.ModelAdmin):
    list_display = ('name','id')