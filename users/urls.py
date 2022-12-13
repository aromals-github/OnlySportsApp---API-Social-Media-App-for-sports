from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import AccountsViewSet,UserProfileViewSet
from . import views


router = routers.DefaultRouter()
router.register('accounts',AccountsViewSet)



urlpatterns = [
    path('create/',include(router.urls)),
    path('user/profile/', views.UserProfileViewSet.as_view()),
]