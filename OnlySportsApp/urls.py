
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_cricket/',include('cricket.urls')),
    path('authentication/',include('users.urls')),
]
