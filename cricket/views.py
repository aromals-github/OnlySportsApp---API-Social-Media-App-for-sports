from rest_framework import viewsets
from .models import CricketPosts
from .serializers import PostSerializer

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny,IsAuthenticated


class CricketPostsViewSet(viewsets.ModelViewSet):
    
    queryset = CricketPosts.objects.all()
    serializer_class = PostSerializer

