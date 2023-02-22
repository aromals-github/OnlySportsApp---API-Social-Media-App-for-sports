from django.urls import path
from .views import *
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('signup/',views.SignUpUserViewSet.as_view()),
    
    path('login/',LoginViewSet.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('user/profile/', views.UserProfileViewSet.as_view()),
    path('logout/', LogoutView.as_view()),
    
    
   
]