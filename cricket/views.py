
from .models import CricketPosts,PostFuntions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import Profile,Accounts
from .backend import createPostFuntions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .hosting_logics.hosting import *



class CricketPostsUploadView(APIView):
    
    queryset                = CricketPosts.objects.all()
    serializer_class        = PostSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)

    def post(self,request,*args,**kwargs):
                    
        try:
            user_logged     = request.user
            user_id         = user_logged.id
           
            if Profile.objects.get(user = user_id):
                profile= Profile.objects.get(user = user_id)
                
                if (('C' in profile.games ) and 
                    ('C' in request.data['context'])) or ('G' in profile.games):
            
                    user_id_logged = Accounts.objects.get(id = user_id)
                    user = CricketPosts.objects.create(user = user_id_logged)
                    serializer = PostSerializer(user,data = request.data)
                    
                    if serializer.is_valid():
                        
                        serializer.save()
                        createPostFuntions()
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
            return Response(status = status.HTTP_307_TEMPORARY_REDIRECT)
    
    
class PostUpdateDeleteView(APIView):
     
    authentication_classes  = (JWTAuthentication,)
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
            return Response({'message':'Your are not the owner of this post'})
        
    def delete(self,request,pk):
        
        logged_in_user  = request.user
        user            = logged_in_user.id
    
        if CricketPosts.objects.filter(id=pk).filter(user=user):
            get_post    = CricketPosts.objects.get(id=pk)
            get_post.delete()
            return Response({'message':'deleted'})
        else:
            return Response({'message':'You are the owner of the post.'}) 
        
        
        
        
class CricketPostLikeFuntion(APIView):
    
    queryset                = PostFuntions.objects.all()
    serializer_class        = PostFuntionSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    
    def post(self,request,pk,*args,**kwargs):
        
        user    = request.user
        userID  =   user.id
        
        if CricketPosts.objects.get(id=pk):
            postCALLED  = PostFuntions.objects.get(post_id=pk)
            
            if postCALLED.likes.filter(id=userID).exists():
                postCALLED.likes.remove(userID)
                return Response({'message':"removed"})
            else:
                postCALLED.likes.add(userID)
                return Response({'message':'added'})
        

class CricketPostDislikeFuntion(APIView):
    
    queryset                = PostFuntions.objects.all()
    serializer_class        = PostFuntionSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    
    def post(self,request,pk,*args,**kwargs):
        
        user    = request.user
        userID  =   user.id
        
        if CricketPosts.objects.get(id=pk):
            
            postCALLED  = PostFuntions.objects.get(post_id=pk)
            
            if postCALLED.dislike.filter(id=userID).exists():
                postCALLED.dislike.remove(userID)
                return Response({'message':"removed"})
            else:
                postCALLED.dislike.add(userID)
                return Response({'message':'added'})
            


class CricketPostViewAllPosts(APIView):
      
    serializer_class        = PostViewSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def get(self,request,*args,**kwargs):
        
        AllPosts        = CricketPosts.objects.all()
        serializer      = PostViewSerializer(AllPosts,many=True)
        context         = {'data':serializer.data}
        return Response(context,status=status.HTTP_302_FOUND)
    
    
class PostInfoViewSet(APIView):
    
    serializer_class        = PostFuntionSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def get(self,request,pk,*args,**kwargs):
        
        getPost     = PostFuntions.objects.get(post_id=pk)
        serializer  = PostFuntionSerializer(getPost)
        return Response({'post review':serializer.data})
    
    
    
    
    
                            # HOSTING TOURNAMENTS
#   ______________________________________________________________________________________                          
                            
                            
                            
                            
    
class HostingTournament(APIView):
    
    serializer_class        = HostTournamentSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def post(self,request,*args,**kwargs):
        
        user        = request.user.id    
        host        = Accounts.objects.get(id= user)
        user        = HostCricketTournaments.objects.create(host=host)
        serializer  = HostTournamentSerializer(user,data = request.data)
        verify_profile  = verify_user(request)
            
        if verify_profile == True:       
            if serializer.is_valid():          
                serializer.save()
                return Response({'data': serializer.data},status = status.HTTP_201_CREATED)             
            else:
                return Response({'errors':serializer.errors},status = status.HTTP_400_BAD_REQUEST)
        
        elif verify_profile == 2:
            return Response("Your are not 18 years old or above to host a tournament")
        
        elif verify_profile == 4:
                return Response("You need to create or update your profile.")    
        
        else:
             return Response({
                 "Your profile is selected for other sports but not as for cricket or as general"
                 })
        
        
    def get(self,request,*args,**kwargs):
        
        all_tournaments = HostCricketTournaments.objects.all()
        serializer      = HostTournamentSerializer(all_tournaments,many=True)
        return Response({"data":serializer.data})
        
             
class TournamentUpdateDelete(APIView):
    
    serializer_class        = TournamentSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = HostCricketTournaments.objects.all()
    
    def put(self,request,pk,*args,**kwargs) :
        
        user        = request.user.id       
        if HostCricketTournaments.objects.filter(id=pk).filter(host=user):
            tournament      = HostCricketTournaments.objects.get(id=pk)
            serializer      = TournamentSerializer(tournament,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data},status=status.HTTP_202_ACCEPTED)
            else :
                return Response({'errors':serializer.errors},status = 
                                        status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Your are not Hosting this tournaments to make any changes."})
           
    def delete(self,request,pk):
        
        user  = request.user.id
        if HostCricketTournaments.objects.filter(id=pk).filter(host=user):
            tournament    = HostCricketTournaments.objects.get(id=pk)
            tournament.delete()
            return Response({'message':'deleted'})
        else:
            return Response({'message':'You are not the owner of the post.'}) 
        
        
class RegistrationViewSet(APIView):
    
    # serializer_class        = 
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def post(self,request,pk,*args,**kwargs):
        
        return Response(status=status.HTTP_100_CONTINUE)