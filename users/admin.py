from django.contrib import admin
from .models import Accounts
from django.contrib.auth.admin import UserAdmin



class AccountsAdmin(UserAdmin):
    list_display        = ('username','email','is_admin','name')
    search_fields       = ('email', 'username')
    readonly_fields     = ('id',)
    
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()
admin.site.register(Accounts,AccountsAdmin)