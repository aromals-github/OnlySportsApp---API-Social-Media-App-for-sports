from django.urls import path
from rest_framework import routers
from django.conf.urls import include

from . import views

# router = routers.DefaultRouter()
# router.register('upload/post',CricketPostsViewSet)




urlpatterns = [
    # path('',include(router.urls)),
    path('upload/post',views.CricketPostsUploadView.as_view()),
]
