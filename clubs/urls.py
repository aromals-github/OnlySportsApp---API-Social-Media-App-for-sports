from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.ResgisterClubViewSet.as_view()),
    
    path('update-delete/<int:pk>',views.ClubUpdateDeleteViewSet.as_view()),
    path('info/<int:pk>/',views.ClubInfoViewSet.as_view()),
    path('club-admins/<int:pk>',views.ClubAdminsViewSet.as_view()),
    
    path('request/membership/<int:pk>/<int:action>',views.ClubMembershipViewSet.as_view()),
   
]
