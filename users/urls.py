from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import AccountsViewSet,UserProfileViewSet


router = routers.DefaultRouter()
router.register('accounts',AccountsViewSet)
router.register('user/profile',UserProfileViewSet)


urlpatterns = [
    path('',include(router.urls)),
]