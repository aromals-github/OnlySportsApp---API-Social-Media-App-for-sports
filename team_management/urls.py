
from django.urls import path
from . import views



urlpatterns =[
    path('team-members/<int:clubID>/<str:sport>/',views.AllClubMembersView.as_view()),
    path('status/update/<int:club>/',views.StatusUpdates.as_view()),
    path('view/all/status/<int:club>',views.MemberStatusView.as_view()),
    path('view/status/<int:club>/<int:user>',views.IndividualPlayerStatus.as_view()),
    
    path('active/cricket/members/<int:club>',views.CricketEligibleList.as_view()),
    path('active/football/members/<int:club>',views.FootballEligibleList.as_view()),
    
    path('set/team/cricket/<int:club>/<int:tournament>/<int:user>',views.SetTeamForCricketMatch.as_view()),
    path('set/team/football/<int:club>/<int:tournament>/<int:user>',views.SetTeamForFootballMatch.as_view()),
    
    
    path('display/cricket-team/<int:club>/<int:tournament>',views.TournamentCricketTeam.as_view()),
    path('display/all/cricket-tournament/team/<int:club>',views.GetAllRegisteredTournament.as_view()),
    path('display/all/football-tournament/team/<int:club>',views.GetAllRegisteredTournament.as_view()),
    
    
    path('annocement/<int:id>',views.Team_Annoncements.as_view()),
    ]
