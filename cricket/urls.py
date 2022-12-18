from django.urls import path
from . import views



urlpatterns = [
    
    path('upload/post',views.CricketPostsUploadView.as_view()),
    path('edit/post/<int:pk>',views.PostUpdateDeleteView.as_view()),
    
]
