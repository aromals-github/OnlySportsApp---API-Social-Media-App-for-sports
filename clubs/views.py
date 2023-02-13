
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from clubs.clubLOGICS.clublogics import clubRepo
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
        get_profile     = Profile.objects.get(user= loggedInUser)
        verifyUser      = clubRepo(request)
        print(get_profile.games)
        
        if (userClub in get_profile.games or 'G' in get_profile.games):
                if verifyUser ==1:
                    user        = Accounts.objects.get(id=loggedInUser)
                    admin       = Clubs.objects.create(owner=user)
                    serializer  = ClubSerializer(admin,data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"Club registered":serializer.data})  
                    else:
                        return Response({'errors':serializer.errors})
                elif verifyUser==0:
                    return Response ({'You are already an owner for a club'})
        else:
            return Response ({"Profile doesn't match with selected game."})
class ClubUpdateDeleteViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ClubUpdateSerializer
    queryset                = Clubs.objects.all()
    
    def put(self,request,pk,*args,**kwargs):
        
        user  = request.user.id
        club = Clubs.objects.get(id=pk)
        if club.owner.id == user:
            serializer = ClubUpdateSerializer(club,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"updated data": serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({"errors":serializer.errors},status=status.HTTP_304_NOT_MODIFIED)
        else:
            return Response({"Not the Owner or an admin for the club."}) 
        
        
    def delete(self,request,pk):
        
        user =  request.user.id
        
        if Clubs.objects.filter(id=pk).filter(owner=user):
            club = Clubs.objects.get(id=pk)
            club.delete()
            return Response({"Deleted"})
        else:
            return Response({"You are no the owner for the club or the Club doesnt not exist"})
        
class ClubInfoViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ClubInfoViewSerializer
    queryset                = Clubs.objects.all()
    
    def get(self,request,pk):
        
        if pk!=0:
            club = Clubs.objects.get(id=pk)
            serializer = ClubInfoViewSerializer(club)
            return Response({"club details": serializer.data})
        elif pk==0:
            AllClubs = Clubs.objects.all()
            serializer = ClubInfoViewSerializer(AllClubs,many=True)
            return Response({"all clubs":serializer.data})
            
class ClubAdminsViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ClubsAdminSerializer
    queryset                = Clubs.objects.all()
    
    def post(self,request,pk):
        
        return Response(status=status.HTTP_100_CONTINUE)
    