
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import Profile,Accounts
# from .backend import createPostFuntions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services import verify_user
from clubs.models import *
  
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
                        serializer.save()
                        Tournament_Notifications.objects.create(tournament=HostCricketTournaments.objects.filter(host=request.user.id).latest('id'))
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
