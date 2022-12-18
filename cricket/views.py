
from .models import CricketPosts
from .serializers import PostSerializer,UpadateDeleteSerializer

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import Profile,Accounts

class CricketPostsUploadView(APIView):
    
    queryset                = CricketPosts.objects.all()
    serializer_class        = PostSerializer
    authentication_classes  = (TokenAuthentication,)
    permission_classes      = (IsAuthenticated,)

    def post(self,request,*args,**kwargs):
        
        try:
            user_logged     = request.user
            user_id         = user_logged.id

            if Profile.objects.get(user = user_id):
                profile= Profile.objects.get(user = user_id)
                
                if ('C' in profile.games ) and ('C' in request.data['context']):
                    
                    user_id_logged = Accounts.objects.get(id = user_id)
                    user = CricketPosts.objects.create(user = user_id_logged)
                    serializer = PostSerializer(user,data = request.data)
                    
                    if serializer.is_valid():
                        
                        serializer.save()
                        return Response({'data': serializer.data},status = 
                                        status.HTTP_201_CREATED)
                    else:
                        
                        return Response({'errors':serializer.errors},status = 
                                        status.HTTP_400_BAD_REQUEST)
                else:
                    
                    response =({'message': 
                        "You can't create a post related to cricket,with your current profile "})
                    return Response(response,status = status.HTTP_403_FORBIDDEN) 
            
        except:
            
            response = ({'message': 'You are not logged in or you dont have an profile'})
            return Response(status = status.HTTP_206_PARTIAL_CONTENT)
    
    
class PostUpdateDeleteView(APIView):
    
    authentication_classes  = (TokenAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = CricketPosts.objects.all()
    serializer_class        = UpadateDeleteSerializer
    
    
    def put(self,request,pk):
        
        logged_in_user  = request.user
        user            = logged_in_user.id
        
        if CricketPosts.objects.filter(id=pk).filter(user=user):
            get_post    = CricketPosts.objects.get(id=pk)
            serializer  = UpadateDeleteSerializer(get_post,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data},status=status.HTTP_202_ACCEPTED)
            else :
                return Response({'errors':serializer.errors},status = 
                                        status.HTTP_400_BAD_REQUEST)
        else:
            
            return Response({'msg':'Your are not the owner of this post'})
        
    def delete(self,request,pk):
        
        logged_in_user  = request.user
        user            = logged_in_user.id
    
        if CricketPosts.objects.filter(id=pk).filter(user=user):
            get_post    = CricketPosts.objects.get(id=pk)
            get_post.delete()
            return Response({'message':'deleted'})
        else:
            return Response({'message':'not deleted'})