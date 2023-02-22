from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Accounts,Profile
from .serializer import SignUpSerializer,ProfileSerializer
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,OutstandingToken 
from .tokens import create_jwt_token
from .services import createClubHistory
class SignUpUserViewSet(APIView):

    serializer_class        = SignUpSerializer
    permission_classes      = []
  
  
    def post(self,request:Request):
        
        data        = request.data
        serializer  = self.serializer_class(data=data) 
        
        if serializer.is_valid():
            serializer.save()
            response =  {
                "message": "User is Created Successfully", "data":serializer.data
            }
            return Response(data = response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
   
   
   
    
class LoginViewSet(APIView):
    
    permission_classes = []
    
    def post(self,request: Request):
         
        email      = request.data.get("email")
        password   = request.data.get("password")
        user       = authenticate(email=email,password=password)
        
        if user is not None:
            
            token       = create_jwt_token(user=user)
            response    = {"message":"logged in","tokens":token}
            return Response(data=response)
        return Response({"message":"credentials are not given ."})
    

class LogoutView(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            if self.request.data.get('all'):
                token: OutstandingToken
                for token in OutstandingToken.objects.filter(user=request.user):
                    _, _ = BlacklistedToken.objects.get_or_create(token=token)
                return Response({"status": "all refresh tokens blacklisted"})
            refresh_token = self.request.data.get('refresh')
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response({"status": "Logged out "})
        except:
            return Response({"Already logged out or Server Error"})
                
class UserProfileViewSet(APIView):
    
    queryset                = Profile.objects.all()
    serializer_class        = ProfileSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    
    def get(self,request,*args,**kwargs):
        
        user    = request.user
        user_id = user.id
        
        try :
            if Profile.objects.filter(user = user_id) :
                database    = Profile.objects.get(user = user_id)
                serializer  = ProfileSerializer(database,many=False)   
                return Response ({'data':serializer.data},status=status.HTTP_302_FOUND)
            
            else :
                response    = {'message':'There is no profile set for this user '}
                return Response(response,status = status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_205_RESET_CONTENT)
                
    
    def post(self,request,*args,**kwargs):  
        
        user_logged   = request.user
        user_id = user_logged.id
        
        try :
            if Profile.objects.filter(user = user_id):
                response = {'message': "You already have a profile set."}
            return Response(response,status=status.HTTP_409_CONFLICT)  
        except: 
             
            id_user     = Accounts.objects.get(id = user_id) 
            user        = Profile.objects.create(user = id_user)
            serializer  = ProfileSerializer(user,data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                createClubHistory(request)
                return Response({'data':serializer.data},status=status.HTTP_202_ACCEPTED)
            
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_403_FORBIDDEN)
       
            
    def put(self, request,*args,**kwargs):
        
        try :
            
            '''contains the logged in user information'''
            user = request.user
            user_id = user.id
            
            if Profile.objects.filter(user=user_id):
                user        = Profile.objects.get(user=user_id)
                serializer  = ProfileSerializer(user,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data},status=status.HTTP_202_ACCEPTED)
                else:
                     return Response({'errors':serializer.errors},
                                     status=status.HTTP_403_FORBIDDEN)  
            else :
                response    = {'message':'There is no existing profile with this user '} 
                return Response (response, status = status.HTTP_204_NO_CONTENT) 
        except:     
           return Response(status=status.HTTP_102_PROCESSING)
    
    
