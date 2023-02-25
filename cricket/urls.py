from django.urls import path
from . import views



urlpatterns = [
    
    # path('upload/post',views.CricketPostsUploadView.as_view()),
    # path('edit/post/<int:pk>',views.PostUpdateDeleteView.as_view()),
    # path('like/post/<int:pk>',views.CricketPostLikeFuntion.as_view()),
    # path('dislike/post/<int:pk>',views.CricketPostDislikeFuntion.as_view()),
    # path('posts',views.CricketPostViewAllPosts.as_view()),
    # path('post/info/<int:pk>',views.PostInfoViewSet.as_view()),
    
    
    #TOURNAMENT HOSTING - URLS
    
    path('host/tournament/',views.HostCricketTournament.as_view()),
    path('update/delete/tournament/<int:pk>',views.TournamentUpdateDelete.as_view()),
    path('tournaments/<int:pk>',views.ListTournamentView.as_view()),
    ]
