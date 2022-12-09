
from rest_framework import viewsets,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Accounts,Profile
from .serializer import AccountSerializer,ProfileSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response



class AccountsViewSet(viewsets.ModelViewSet):
    
    queryset                = Accounts.objects.all()
    serializer_class        = AccountSerializer
    permission_classes      = (AllowAny,)
    


class UserProfileViewSet(viewsets.ModelViewSet):
    
    queryset                = Profile.objects.all()
    serializer_class        = ProfileSerializer
    authentication_classes  = (TokenAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    @action(detail=True, methods=['POST'])
    def profile_updates(self,request,pk):
       
        if 'games' in request.data:
            print('ok')
        
        
    