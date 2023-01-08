
from django.contrib import admin
from django.urls import path
from django.conf.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('authentication/',include('users.urls')),
    
    path('api/cricket/',include('cricket.urls')),
    path('api/football/' ,include('football.urls')),
    
]


