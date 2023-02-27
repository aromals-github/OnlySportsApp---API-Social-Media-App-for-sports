
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import Profile,Accounts
# from .backend import createPostFuntions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services import *
from clubs.models import *
from clubs.services import *



class HostCricketTournament(APIView):
    
    serializer_class        = HostTournamentSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = HostCricketTournaments.objects.all()
    
    
    def post(self,request,*args,**kwargs):
       try: 
            store_district  = request.data['district']
            store_date      = request.data['date']
            if HostCricketTournaments.objects.filter(host=request.user.id,date=store_date,district = store_district):
                 return Response({"Error":"You are already hosting a tournament on the same district in the same date."})
            else:
                verify_profile  = verify_user(request)
                if verify_profile == True:
                    account         = Accounts.objects.get(id=request.user.id)
                    user            = HostCricketTournaments.objects.create(host=account)
                    serializer      = HostTournamentSerializer(user,data = request.data)       
                    if serializer.is_valid():         
                        d = serializer.save()
                        Resgister_Tournaments.objects.create(tournament=d)
                        Tournament_Notifications.objects.create(tournament=d)
                        Tournament_Reports.objects.create(tournament=d)
                        return Response({'data': serializer.data},status = status.HTTP_201_CREATED)             
                    else:
                        return Response({'errors':serializer.errors},status = status.HTTP_400_BAD_REQUEST)
                elif verify_profile == 2:
                    return Response({"Age Restriction":"Your are not 18 years old or above to host a tournament"})
                elif verify_profile == 4:   
                    return Response({"Profile Not Found":"Create a user profile or update your user profile to host a tournament."})    
                else:
                    return Response({"Your profile is selected for other sports item but not as for cricket "})
               
       except:
           return Response({"Error":"Server Error "})
       
class ListTournamentView(APIView):
    
    serializer_class        = TournamentViewSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    quertset                = HostCricketTournaments.objects.all()
    
    def get(self,request,pk):
        
        try:
            if pk == 0:
                tournament = HostCricketTournaments.objects.all()
                serializer = TournamentViewSerializer(tournament,many=True)
                return Response({"All Tournaments":serializer.data})
            else:
                if HostCricketTournaments.objects.filter(id=pk):
                    tournament = HostCricketTournaments.objects.get(id=pk)
                    serializer = TournamentViewSerializer(tournament,many=False)
                    return Response({"Tournament":serializer.data})
                else:
                    return Response({"NOT FOUND ":"Tournament not found."})
        except:
            return Response({"Error":"Server Error"})                 
            
class TournamentUpdateDelete(APIView):
    
    serializer_class        = TournamentSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = HostCricketTournaments.objects.all()
    
    def put(self,request,pk,*args,**kwargs) :
    
        try:
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
        except:
            return Response({"Error":"Server Error"})
           
    def delete(self,request,pk):
        try:
            if HostCricketTournaments.objects.filter(id=pk):
                if HostCricketTournaments.objects.filter(id=pk,host=request.user.id):
                    if Tournament_Notifications.objects.filter(tournament=pk,cancelled=False):
                        Tournament_Notifications.objects.update(tournament=pk,cancelled=True,verified=False)
                        return Response({"Sucess Message":"Tournament Cancelled"})
                    else:
                        return Response({"Error Message":"Already Cancelled"})
                else:
                    return Response({"User Error":"You are not the host for the given tournament."})
            else:
                return Response({"Tournament not found"})
        except:
            return Response({"Error":"Server Error"})



class ReportTournament(APIView):
    
    serializer_class        = TournamentSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = HostCricketTournaments.objects.all()
    
    def post(self,request,pk):
        try:
            if HostCricketTournaments.objects.filter(id=pk,host=request.user.id):
                return Response({"Error":"You cannot report your own tournament."})
            else:
                if Tournament_Reports.objects.filter(tournament=pk,reporters = request.user.id):
                    return Response({"Success":"Already reported"})
                else:
                    get = Tournament_Reports.objects.get(tournament=pk)
                    get.reporters.add(request.user.id)
                    report_action(pk)
                    return Response({"Success":"You have reported the tournament as inadequate."})
        except:
            return Response({"Error":"Server Error"})
        
class TournamentRegistration(APIView):
    
    serializer_class        = TournamentSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = HostCricketTournaments.objects.all()
    
    def post(self,request,pk):
        createClubHistory(request)
        try:
            if HostCricketTournaments.objects.filter(id=pk):
                if Tournament_Notifications.objects.filter(tournament=pk,verified =True):
                    user_history = ClubHistoryPerUser.objects.get(user=request.user.id)
                    if user_history.owner == True: 
                        getClub = Clubs.objects.get(owner=request.user.id)
                        if Resgister_Tournaments.objects.filter(tournament=pk,registered=getClub.id):
                            return Response({"Success":"Your club is already registered for the tournament."})
                        else:    
                            registration = Resgister_Tournaments.objects.get(tournament=pk)
                            registration.registered.add(getClub.id)
                            getTournament = HostCricketTournaments.objects.get(id=pk)
                            getTournament.registered_teams.add(getClub.id)
                            return Response({"Success":"Club Registered for the tournament"})
                    elif ((user_history.club_admin.filter())):
                        getClub = user_history.club_admin.get()
                        if Resgister_Tournaments.objects.filter(tournament=pk,registered=getClub.id):
                            return Response({"Success":"Your club is already registered for the tournament."})
                        else:
                            registration = Resgister_Tournaments.objects.get(tournament=pk)
                            registration.registered.add(getClub.id)
                            getTournament = HostCricketTournaments.objects.get(id=pk)
                            getTournament.registered_teams.add(getClub.id)
                            return Response({"Success":"Club Registered for the tournament"})
                    else:
                        return Response({"Registration Error":"You are not an Owner or an admin for any club"})
                else:
                    return Response({"Error":"Tournament is either been cancelled or reported as inadequate."})   
            else:
                return Response({"Error": "Tournament not found"})
        except:
            return Response({"Error":"Server Error"})
        
        
    def delete(self,request,pk):
        
        try:
            if HostCricketTournaments.objects.filter(id=pk):
                if Tournament_Notifications.objects.filter(tournament=pk):
                    user_history = ClubHistoryPerUser.objects.get(user=request.user.id)
                    if user_history.owner == True: 
                        getClub = Clubs.objects.get(owner=request.user.id)
                        if Resgister_Tournaments.objects.filter(tournament=pk,registered=getClub.id):
                            registration = Resgister_Tournaments.objects.get(tournament=pk)
                            registration.registered.remove(getClub.id)
                            getTournament = HostCricketTournaments.objects.get(id=pk)
                            getTournament.registered_teams.remove(getClub.id)
                            return Response({"Success":"Registration Cancelled."})
                        else:    
                            return Response({"Success":"Already Cancelled"})
                        
                    elif ((user_history.club_admin.filter())):
                        getClub = user_history.club_admin.get()
                        if Resgister_Tournaments.objects.filter(tournament=pk,registered=getClub.id):
                            registration = Resgister_Tournaments.objects.get(tournament=pk)
                            registration.registered.remove(getClub.id)
                            getTournament = HostCricketTournaments.objects.get(id=pk)
                            getTournament.registered_teams.remove(getClub.id)
                            return Response({"Success":"Registration Cancelled."})
                        else:
                            return Response({"Success":"Already Cancelled"})
                    else:
                        return Response({"Cancellation Error":"You are not an Owner or an admin for any club"})
                else:
                    return Response({"Error":"Tournament is either been cancelled or reported as inadequate."})   
            else:
                return Response({"Error": "Tournament not found"})
        except:
            return Response({"Error":"Server Error"}) 