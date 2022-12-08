from rest_framework import viewsets
from .models import CricketPosts
from .serializers import PostSerializer


class CricketPostsViewSet(viewsets.ModelViewSet):
    
    queryset = CricketPosts.objects.all()
    serializer_class = PostSerializer

