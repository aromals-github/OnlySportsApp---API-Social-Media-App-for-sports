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



class StatusUpdates(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = MemberStatus.objects.all()
    
    def post(self,request,club,status):
        
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
                if status==0:
                   MemberStatus.objects.filter(club=club,member=request.user.id,status=True).update(status=False)
                   return Response({"Success":"Status updated."})
                elif status==1:
                    MemberStatus.objects.filter(club=club,member=request.user.id,status=False).update(status=True)
                    return Response({"Success":"Status updated."})
                else:
                    return Response({"Error":"status request not found"})
            else:   
                return Response({"Error":"Not a member for the club"})
        except:
            return Response({"Error":"Server Error"})

class CricketEligibleList(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = MemberStatus.objects.all()
    
    def get(self,request,club):
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
                club = Clubs.objects.get(id=club)
                list = []
                for user in club.members.all():
                    if Profile.objects.filter(user=user,games='A')or Profile.objects.filter(user=user,games='C'):
                        list.append(user.id)
                no_of_members = len(list)
                serializied_data = []
                for user in range(no_of_members):
                    getProfile = Accounts.objects.get(id=list[user])
                    serializer = AccountSerializer(getProfile)
                    serializied_data.append(serializer.data)
                return Response({"data":serializied_data})
                
            else:
                return Response({"Error":"Not a member for the club."})
        except:
            return Response ({"Error":"Server Error"})
        
class FootballEligibleList(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = MemberStatus.objects.all()
    
    def get(self,request,club):
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
                club = Clubs.objects.get(id=club)
                list = []
                for user in club.members.all():
                    if Profile.objects.filter(user=user,games='A')or Profile.objects.filter(user=user,games='F'):
                        list.append(user.id)
                no_of_members = len(list)
                serializied_data = []
                for user in range(no_of_members):
                    getProfile = Accounts.objects.get(id=list[user])
                    serializer = AccountSerializer(getProfile)
                    serializied_data.append(serializer.data)
                return Response({"data":serializied_data})
                
            else:
                return Response({"Error":"Not an Member  for the club."})
        except:
            return Response ({"Error":"Server Error"})
        
class MemberStatusView(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = MemberStatus.objects.all()
    serializer_class        = StatusSerializer
    
    def get(self,request,club):
        
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
                status = MemberStatus.objects.filter(club=club).all()
                serializer =  StatusSerializer(status,many=True)
                return Response({"Status":serializer.data})
            else:
                 return Response({"Error":"Not the owner or an member for the club."}) 
        except:
            return Response({"Error":"Server Error"})
                
class SetTeamForCricketMatch(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = ClubCricketMembers.objects.all()
    
    def post(self,request,club,tournament,user):
        
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,admins=request.user.id):
                if ClubCricketMembers.objects.filter(club=club,tournament=tournament,active=True):
                    if MemberStatus.objects.filter(club=club,member=user,status=True):
                        cricket_team = ClubCricketMembers.objects.get(club=club,tournament=tournament)
                        if ClubCricketMembers.objects.filter(tournament=tournament,club=club,players=user):
                            
                            return Response({"Success":"Already in team."})
                        else:
                            cricket_team.players.add(user)
                            return Response({"Success":"Player added."})
                    else:
                        return Response({"Error":"Player status is 'NOT AVAILABLE'."})
                else:
                    return Response({"Message":"The Tournament has been cancelled or reported as inadquate."})
            else:
                return Response({"Error":"Not an owner or an admin to select a team."})
        except:
            return Response({"Error":"Server Error"})
        
    def delete(self,request,club,tournament,user):
        
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,admins=request.user.id):
                if ClubCricketMembers.objects.filter(club=club,tournament=tournament,active=True):
                    if MemberStatus.objects.filter(club=club,member=user,status=True):
                        cricket_team = ClubCricketMembers.objects.get(club=club,tournament=tournament)
                        if ClubCricketMembers.objects.filter(tournament=tournament,club=club,players=user):
                            cricket_team.players.remove(user)
                            return Response({"Success":"Player has been removed from the tournament team."})
                        else:
                            return Response({"Success":"Never added or removed already."})
                    else:
                        return Response({"Error":"Player status is 'NOT AVAILABLE'."})
                else:
                    return Response({"Message":"The Tournament has been cancelled or reported as inadquate."})
            else:
                return Response({"Error":"Not an owner or an admin to select a team."})
        except:
            return Response({"Error":"Server Error"})
        
class SetTeamForFootballMatch(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = ClubFootballMembers.objects.all()
    
    def post(self,request,club,tournament,user):
        
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,admins=request.user.id):
                if ClubFootballMembers.objects.filter(club=club,tournament=tournament,active=True):
                    if MemberStatus.objects.filter(club=club,member=user,status=True):
                        football_team = ClubFootballMembers.objects.get(club=club,tournament=tournament)
                        if ClubFootballMembers.objects.filter(tournament=tournament,club=club,players=user):
                            return Response({"Success":"Already added."})
                        else:
                            football_team.players.add(user)
                            return Response({"Success":"Player added."})
                    else:
                        return Response({"Error":"Player status is 'NOT AVAILABLE'."})
                else:
                    return Response({"Message":"The Tournament has been cancelled or reported as inadquate."})
            else:
                return Response({"Error":"Not an owner or an admin to select a team."})
        except:
            return Response({"Error":"Server Error"})
        
    def delete(self,request,club,tournament,user):
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,admins=request.user.id):
                if ClubFootballMembers.objects.filter(club=club,tournament=tournament,active=True):
                    if MemberStatus.objects.filter(club=club,member=user,status=True):
                        football_team = ClubFootballMembers.objects.get(club=club,tournament=tournament)
                        if ClubFootballMembers.objects.filter(tournament=tournament,club=club,players=user):
                            football_team.players.remove(user)
                            return Response({"Success":"Removed."})
                        else:
                            return Response({"Success":"Never added or removed already"})
                    else:
                        return Response({"Error":"Player status is 'NOT AVAILABLE'."})
                else:
                    return Response({"Message":"The Tournament has been cancelled or reported as inadquate."})
            else:
                return Response({"Error":"Not an owner or an admin to select a team."})
        except:
            return Response({"Error":"Server Error"})
        
        
        
class IndividualPlayerStatus(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = MemberStatus.objects.all()
    serializer_class        = StatusSerializer
    
    def get(self,request,user,club):
        
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
                if Clubs.objects.filter(members=user):
                    status = MemberStatus.objects.get(club=club,member=user)
                    serializer = StatusSerializer(status)
                    return Response({"Status":serializer.data})
                else:
                    return Response({"Error":"This person is not in your club"})
            else:
                return Response({"Error":"You are not a member of the club."})
        except:
            return Response({"Error":"Server Error"})
        
class TournamentCricketTeam(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = ClubCricketMembers.objects.all()
    serializer_class        = CricketTeamSerializer
    
    def get(self,request,club,tournament):
         
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
                if  ClubCricketMembers.objects.filter(club=club,tournament=tournament,active=True):
                    get_members = ClubCricketMembers.objects.get(club=club,tournament=tournament,active=True)
                    serializer  = CricketTeamSerializer(get_members)
                    return Response({"Team":serializer.data})
                else:
                    return Response({"Error":"Tournament not registered or cancelled."})
            else:
                return Response({"Error":"You are not an member for the club"})
        except:
            return Response({"Error":"Server Error"})

class GetAllRegisteredTournament(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = ClubCricketMembers.objects.all()
    serializer_class        = CricketTeamSerializer
    
    def get(self,request,club):
        
        if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
            getAll = ClubCricketMembers.objects.filter(active=True).all()
            serializer = CricketTeamSerializer(getAll,many=True)
            return Response({"Registered Tournaments":serializer.data})
            
        else:
            return Response({"Error":"Not an owner or an member for the club."})
        
        
        
class TournamentCricketTeam(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = ClubFootballMembers.objects.all()
    serializer_class        = FootballTeamSerializer
    
    def get(self,request,club,tournament):
         
        try:
            if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
                if  ClubFootballMembers.objects.filter(club=club,tournament=tournament,active=True):
                    get_members = ClubFootballMembers.objects.get(club=club,tournament=tournament,active=True)
                    serializer  = FootballTeamSerializer(get_members)
                    return Response({"Team":serializer.data})
                else:
                    return Response({"Error":"Tournament not registered or cancelled."})
            else:
                return Response({"Error":"You are not an member for the club"})
        except:
            return Response({"Error":"Server Error"})

class GetAllRegisteredTournament(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = ClubFootballMembers.objects.all()
    serializer_class        = FootballTeamSerializer
    
    def get(self,request,club):
        
        if Clubs.objects.filter(id=club,owner=request.user.id) or Clubs.objects.filter(id=club,members=request.user.id):
            getAll = ClubFootballMembers.objects.filter(active=True).all()
            serializer = FootballTeamSerializer(getAll,many=True)
            return Response({"Registered Tournaments":serializer.data})
            
        else:
            return Response({"Error":"Not an owner or an member for the club."})