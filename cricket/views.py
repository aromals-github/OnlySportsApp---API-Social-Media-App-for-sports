# from rest_framework import viewsets
from .models import CricketPosts
from .serializers import PostSerializer

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated


class CricketPostsUploadView(APIView):
    
    queryset            = CricketPosts.objects.all()
    serializer_class    = PostSerializer
    permission_classes  = (AllowAny,)

    def get(self,*args,**kwargs):
        
        response = { 'msg': 'hello' }
        return Response(response)
    
    def post(self,request,*args,**kwargs):
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data},status = status.HTTP_201_CREATED)
        else:
            return Response({'errors':serializer.errors},status = status.HTTP_400_BAD_REQUEST)