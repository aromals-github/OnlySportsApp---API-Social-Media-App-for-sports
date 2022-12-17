from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny,IsAuthenticated

from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Accounts,Profile
from .serializer import AccountSerializer,ProfileSerializer

class AccountsViewSet(viewsets.ModelViewSet):
    
    queryset                = Accounts.objects.all()
    serializer_class        = AccountSerializer
    permission_classes      = (AllowAny,)
    
class UserProfileViewSet(APIView):
    
    queryset                = Profile.objects.all()
    serializer_class        = ProfileSerializer
    authentication_classes  = (TokenAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    
    def get(self,request,*args,**kwargs):
        
        user    = request.user
        user_id = user.id
        try :
            if Profile.objects.filter(user = user_id) :
                
                database    = Profile.objects.get(user = user_id)
                serializer  = ProfileSerializer(database, many=False)   
                return Response ({'data':serializer.data},status=status.HTTP_302_FOUND)
            
            else :
                
                response    = {'message':'There is no profile for this user '}
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
       