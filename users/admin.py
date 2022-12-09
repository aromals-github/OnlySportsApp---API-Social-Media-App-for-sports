from django.contrib import admin
from .models import Accounts,Profile
from django.contrib.auth.admin import UserAdmin



class AccountsAdmin(UserAdmin):
    
    list_display        = ('username','email','is_admin','name')
    search_fields       = ('email', 'username')
    readonly_fields     = ('id',)
    
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()
admin.site.register(Accounts,AccountsAdmin)


@admin.register(Profile)
class ProfileHolder(admin.ModelAdmin):
    list_display        = ('games','user')


