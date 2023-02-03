
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from users.models import Profile
from .serializers import *


class ResgisterClubViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ClubSerializer
    queryset                = Clubs.objects.all()
    
    def post(self,request,*args,**kwargs):
        
        loggedInUser    = request.user.id
        userClub        = request.data['games']
        
        try:
            get_profile     = Profile.objects.get(user= loggedInUser)
            if userClub in get_profile.games:
                
                user        = Accounts.objects.get(id=loggedInUser)
                admin       = Clubs.objects.create(owner=user)
                serializer  = ClubSerializer(admin,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'created'})  
                else:
                    return Response({'errors':serializer.errors})
            else:
                return Response ( {'Your profile doesnt contain the game inorder to create a club with this particular game'})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)