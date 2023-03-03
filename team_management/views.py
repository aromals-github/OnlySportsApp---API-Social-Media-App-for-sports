from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import Profile,Accounts
from django.db.models import Q


class AllClubMembersView(APIView):
    
    serializer_class        = AllClubMemberSerializer,AccountSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = Clubs.objects.all()
    
    def get(self,request,clubID,sport):
        try:
            if Clubs.objects.filter(id=clubID,owner=request.user.id) or Clubs.objects.filter(id=clubID,members=request.user.id):
                if (sport == 'all'):
                    getAllMembers = Clubs.objects.filter(id=clubID)
                    serializer = AllClubMemberSerializer(getAllMembers,many=True)
                    return Response({"Members":serializer.data})
                elif (sport =='cricket'):
                    club = Clubs.objects.get(id=clubID)
                    list = []
                    for user in club.members.all():
                        if Profile.objects.filter(user=user,games='C'):
                            list.append(user.id)
                    no_of_members = len(list)
                    serializied_data = []
                    for user in range(no_of_members):
                        getProfile = Accounts.objects.get(id=list[user])
                        serializer = AccountSerializer(getProfile)
                        serializied_data.append(serializer.data)
                    return Response({"data":serializied_data})
                elif(sport=='football'):
                    club = Clubs.objects.get(id=clubID)
                    list = []
                    for user in club.members.all():
                        if Profile.objects.filter(user=user,games='F'):
                            list.append(user.id)
                    no_of_members = len(list)
                    serializied_data = []
                    for user in range(no_of_members):
                        getProfile = Accounts.objects.get(id=list[user])
                        serializer = AccountSerializer(getProfile)
                        serializied_data.append(serializer.data)
                    return Response({"data":serializied_data})
                elif(sport=='general'):
                    club = Clubs.objects.get(id=clubID)
                    list = []
                    for user in club.members.all():
                        if Profile.objects.filter(user=user,games='A'):
                            list.append(user.id)
                    no_of_members = len(list)
                    serializied_data = []
                    for user in range(no_of_members):
                        getProfile = Accounts.objects.get(id=list[user])
                        serializer = AccountSerializer(getProfile)
                        serializied_data.append(serializer.data)
                    return Response({"data":serializied_data})
                else:
                    return Response({"Not Found":"Sports item is not valid"})
            else:
                return Response({"Error":"You are not the owner or a member of the club to view club information "})
        except:
            return Response({"Error":"Server Error"})


