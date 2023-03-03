
from django.urls import path
from . import views



urlpatterns =[
    path('team-members/<int:clubID>/<str:sport>/',views.AllClubMembersView.as_view()),
    ]
