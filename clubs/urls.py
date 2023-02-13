from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.ResgisterClubViewSet.as_view()),
    path('update-delete/<int:pk>',views.ClubUpdateDeleteViewSet.as_view()),
    path('info/<int:pk>/',views.ClubInfoViewSet.as_view()),
    path('club-admins/',views.ClubAdminsViewSet.as_view())
   
]
