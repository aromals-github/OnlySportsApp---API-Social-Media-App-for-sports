
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_cricket/',include('cricket.urls')),
    path('authentication/',include('users.urls')),
]
