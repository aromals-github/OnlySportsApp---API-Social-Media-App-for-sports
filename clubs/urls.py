from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.CreateClubViewSet.as_view()),
    path('update/delete/<int:pk>',views.ClubUpdateDeleteViewSet.as_view()),
    path('club-info/<int:pk>',views.ClubInfoViewSet.as_view()), # GET
    
    path('request/membership/<int:pk>/<int:action>',views.ClubMembershipViewSet.as_view()),
    path('response/membership/<int:pk>/<int:user>/<int:action>',views.ClubMembershipResponse.as_view()),
    
    path('member/remove/<int:club>/<int:removee>',views.RemoveMemberClubViewSet.as_view()),
    
    path('membership/requests/<int:pk>',views.ViewAllRequestsViewSet.as_view()),
    path('admins/add-remove/<int:pk>/<int:user>',views.ClubAdminsViewSet.as_view()),
]
