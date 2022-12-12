
from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Accounts,Profile
from .serializer import AccountSerializer,ProfileSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

class AccountsViewSet(viewsets.ModelViewSet):
    
    queryset                = Accounts.objects.all()
    serializer_class        = AccountSerializer
    permission_classes      = (AllowAny,)
    


class UserProfileViewSet(APIView):
    
    queryset                = Profile.objects.all()
    serializer_class        = ProfileSerializer
    authentication_classes  = (TokenAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    
    
    def post(self,request,*args,**kwargs):  
        
        try :
            if Profile.objects.get(user=request.user):
                response = {'message': "You already have a game selected...."}
                return Response(response,status=status.HTTP_409_CONFLICT)  
        except:     
            serializer = ProfileSerializer(data=request.data)
            print (request.data['user'])
            
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_403_FORBIDDEN)