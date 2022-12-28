from django.urls import path

from . import views


urlpatterns = [
   path('upload/post',views.FootballPostViewSet.as_view()),
]
