from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin



class AccountsAdmin(UserAdmin):
    
    list_display        = ('username','email','is_admin','id')
    search_fields       = ('email', 'username')
    readonly_fields     = ('id',)
    
    filter_horizontal   = ()
    list_filter         = ('date_joined','is_admin',)
    fieldsets           = ()
admin.site.register(Accounts,AccountsAdmin)


@admin.register(Profile)
class ProfileHolder(admin.ModelAdmin):
    list_display        = ('user','name','age','district')
    search_fields       = ('user','district')
    filter_horizontal   = ()
    list_filter         = ('district',)
    fieldsets           = ()
    


