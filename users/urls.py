from django.urls import path
from .views import *
from . import views



urlpatterns = [
    path('signup/',views.SignUpUserViewSet.as_view()),
    path('login/',views.LoginViewSet.as_view()),
    path('user/profile/', views.UserProfileViewSet.as_view()),
]