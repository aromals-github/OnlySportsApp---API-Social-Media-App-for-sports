from django.urls import path
from . import views



urlpatterns =[
    
    path('host/tournament/',views.HostCricketTournament.as_view()),
    path('update/delete/tournament/<int:pk>',views.TournamentUpdateDelete.as_view()),
    path('tournaments/<int:pk>',views.ListTournamentView.as_view()),
    path('register/cancel/tournament/<int:pk>',views.TournamentRegistration.as_view()),
    ]
