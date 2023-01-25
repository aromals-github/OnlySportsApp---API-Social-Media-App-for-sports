from django.urls import path
from . import views



urlpatterns = [
    
    path('upload/post',views.CricketPostsUploadView.as_view()),
    path('edit/post/<int:pk>',views.PostUpdateDeleteView.as_view()),
    path('like/post/<int:pk>',views.CricketPostLikeFuntion.as_view()),
    path('dislike/post/<int:pk>',views.CricketPostDislikeFuntion.as_view()),
    path('posts',views.CricketPostViewAllPosts.as_view()),
    path('post/info/<int:pk>',views.PostInfoViewSet.as_view()),
    
    
     path('host-tournament/',views.HostingTournament.as_view()),
    
    
    
    
]
