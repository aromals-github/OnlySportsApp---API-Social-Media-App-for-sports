
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import Profile
from .serializers import *
from .services import *
from team_management.models import Club_Games_History,MemberStatus
class CreateClubViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ClubSerializer
    queryset                = Clubs.objects.all()
    
    def post(self,request,*args,**kwargs):
        
        try:
            loggedInUser     = request.user.id
            userGames        = request.data['games']
            get_profile      = Profile.objects.get(user= loggedInUser)
            createClubHistory(request)
            verifyUser      = clubRepo(request)

            if((userGames in get_profile.games ) or ('A' in get_profile.games)):
                    if verifyUser == 1:
                        user        = Accounts.objects.get(id=loggedInUser)
                        admin       = Clubs.objects.create(owner=user)
                        serializer  = ClubSerializer(admin,data=request.data)
                        if serializer.is_valid():
                            d = serializer.save()
                            Club_Games_History.objects.create(club=d)
                            updateClubHistory(request)
                            MemberStatus.objects.create(club=d,member=request.user.id)
                            return Response({"Club created":serializer.data})  
                        else:
                            return Response({'errors':serializer.errors})
                    elif verifyUser==0:
                        return Response ({"Condition 1":'No more than one club can be created by a single user at a time.',
                                          "Condition 2":'Cannot be admin for any other club.',
                                          "Condition 3":'Cannot be member for any other club.',
                                          "Requirement":'Meet all condition by above.'})
            else:
                return Response ({"Error":"Profile  doesn't match with selected game."})
        except:
            return Response ({"Error":"Server Error"})
        
        
class ClubUpdateDeleteViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ClubUpdateSerializer
    queryset                = Clubs.objects.all()
    
    def put(self,request,pk):
        try:
            if Clubs.objects.filter(id=pk):
                getClub = Clubs.objects.get(id=pk)
                if getClub.owner.id == request.user.id:
                    serializer  = ClubUpdateSerializer(getClub,data=request.data,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"updated data": serializer.data},status=status.HTTP_200_OK)
                    else:
                        return Response({"Errors":serializer.errors},status=status.HTTP_304_NOT_MODIFIED)
                else:
                    return Response ({"Error":"Only Owner of the Club can edit club Stats."})
            else:
                return Response({"Error":"Club does not Exists."})
        except:
            return Response({"Error":"Server Error"})
        
        
    def delete(self,request,pk):
       try: 
            user =  request.user.id
            if Clubs.objects.filter(id=pk).filter(owner=user):
                club = Clubs.objects.get(id=pk)
                club.delete()
                ClubHistoryPerUser.objects.filter(user=request.user.id).update(owner=False)
                return Response({"Success":"Deleted"})
            else:
                return Response({"Error":"You are not the owner for the club or the Club doesnt not exist"})  
       except:
           return Response({"Error":"Server Error"})
class ClubInfoViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = ClubInfoViewSerializer
    queryset                = Clubs.objects.all()
    
    def get(self,request,pk):
        try:
            if pk != 0:
                if Clubs.objects.filter(id=pk):
                    club = Clubs.objects.get(id=pk)
                    serializer = ClubInfoViewSerializer(club)
                    return Response({"club details": serializer.data})
                else:
                    return Response({"Error":"No club exists"})
            
            elif pk==0:
                AllClubs = Clubs.objects.all()
                serializer = ClubInfoViewSerializer(AllClubs,many=True)
                return Response({"all clubs":serializer.data})
        except:
            return Response({"Error":"Unknown error"})
        
class ClubMembershipViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = MembershipRequest.objects.all()
    

    def post(self,request,pk,action): 
        
        try:
            createClubHistory(request)
            getHistoryUser = ClubHistoryPerUser.objects.get(user=request.user.id)
            getProfile     = Profile.objects.get(user=request.user.id)
            getClub        = Clubs.objects.get(id=pk)
            if(('A' in getClub.games) or ('A' in getProfile.games) or (getProfile.games==getClub.games)):
                if getHistoryUser.owner == False:
                    
                    if getHistoryUser.total_admin() < 1:
                    
                        if getHistoryUser.total_membership() >= 5:
                            return Response({"Error":"You are member in 5 clubs,exit from another club to join new"})
                        else:
                            
                            if Clubs.objects.get(id=pk):
                            
                                if MembershipResponses.objects.filter(club=pk,blocked=request.user.id):
                                    return Response({"Status":"You are blocked"})
                                else:
                                    
                                    list_created = membershipList(request,pk) ; '''CREATE LIST FOR MEMBERS'''
                                    if action == 1:
                                        user    = request.user.id 
                                        account = Accounts.objects.get(id=user)
                                        club_requested = Clubs.objects.get(id=pk)
                                    
                                        if MembershipRequest.objects.filter(club=club_requested).filter(is_active=True).filter(sender=user):  
                                            return Response ({"Status":"Request is pending"})
                                    
                                        else:
                                            if MembershipRequest.objects.filter(club=pk).filter(is_active=False).filter(sender=user):
                                                return Response({"Status":"You are already a member for the club"})
                                            else:
                                                if list_created == False:
                                                    return Response({"User Error":"You are the owner for the club."})
                                                else:
                                                    instance = MembershipRequest(club=club_requested,sender=account)
                                                    instance.save()
                                                    return Response({"Status":"Requested"})
                                
                                    elif action == 0:
                                        user            = request.user.id 
                                        account         = Accounts.objects.get(id=user)
                                        club_requested  = Clubs.objects.get(id=pk)

                                        if MembershipRequest.objects.filter(club=club_requested).filter(is_active=True).filter(sender=user): 
                                            instance = MembershipRequest.objects.get(club=club_requested,sender=account) 
                                            instance.delete()
                                            return Response ({"Status":"Cancelled"})
                                        else:
                                            return Response(status=status.HTTP_400_BAD_REQUEST)
                                
                                    else:
                                        return Response({"error":"URL-/<int:action> || value should be 1 (Send Request) or 0 (Cancel Request)."})
                            else:
                                return Response({"Club doesnt exist."})
                    else:
                        return Response({"Error":"You are an admin for a differnet club."})
                else:
                    return Response ({"Error":" You own a club, an owner cannot request for membership in another clubs."})      
            else:
                return Response({"Error":"Check the Club games and verify that your  profile matches the club requirement."})
        except:
             return Response({"ERROR WITH SELECTED CLUB":"This club is either terminated or never existed."})   
         
          

class ClubMembershipResponse(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = Clubs.objects.all()
    
    def post(self,request,pk,user,action):
        try:
            if MembershipResponses.objects.filter(club=pk):
                club = Clubs.objects.get(id=pk)
                
                if ((club.owner.id == request.user.id)or(Clubs.objects.filter(id=pk,admins=request.user.id))) :
                    account = Accounts.objects.get(id=user)
                    if action == 1:
                        getHistory  = ClubHistoryPerUser.objects.get(user=user)
                        if (getHistory.total_membership() < 5 and getHistory.total_admin() < 1):
                            if MembershipRequest.objects.get(club=pk,sender=account,is_active=True):
                                membership_model_accepted = MembershipRequest.objects.get(club=pk,sender=account,is_active=True)
                                membership_model_accepted.delete()
                                club_requested = Clubs.objects.get(id=pk)
                                new_instance_accepted = MembershipRequest(club=club_requested,sender=account,is_active=False)
                                new_instance_accepted.save()
                            response_model_accepted = MembershipResponses.objects.get(club=pk)
                            response_model_accepted.waiting.remove(user)
                            response_model_accepted.accepted.add(user)
                            club_model_accepted = Clubs.objects.get(id=pk)
                            club_model_accepted.members.add(user)
                            updateHistory = ClubHistoryPerUser.objects.get(user=user)
                            updateHistory.club_member.add(club_requested)
                            MemberStatus.objects.create(club=pk,member=user)
                            return Response({"Status":"Accepted"})
                        else:
                            return Response({"Condition Error":"Requested User is already a member of 5 clubs.",
                                             "Condition Error":"Requested User is Admin for more than 1 club."})
                    
                    elif action == 0:
                        
                        response_model_declined = MembershipResponses.objects.get(club=pk)
                        response_model_declined.waiting.remove(user)
                        membership_model_declined = MembershipRequest.objects.get(club=pk,sender=account,is_active=True)
                        membership_model_declined.delete()
                        return Response({"Status":"Declined"})
                    
                    elif action == 2 :
                        response_model_blocked = MembershipResponses.objects.get(club=pk)
                        response_model_blocked.waiting.remove(user)
                        response_model_blocked.blocked.add(user)
                        membership_model_blocked = MembershipRequest.objects.get(club=pk,sender=account,is_active=True)
                        membership_model_blocked.delete()
                        return Response({"Status":"Blocked"})
            
                    else:
                        return Response({"Error":" Action request is invalid in the url."})
                else:
                    return Response({"Error":"Only owner and club admins can accept and decline memebership requests."})
            else:
                return Response({"Error":"Club does not exists."})
        except:
            return Response({"Error": "Server error"})

class RemoveMemberClubViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = Clubs.objects.all()
    
    def post(self,request,club,removee):
        try:
            if Clubs.objects.get(id=club):
                getClub = Clubs.objects.get(id=club)
                if ((getClub.owner.id == request.user.id)or(Clubs.objects.filter(id=club,admins=request.user.id))):
                    if Clubs.objects.filter(id=club).filter(members=removee):
                        club_called = Clubs.objects.get(id=club)
                        club_called.members.remove(removee)
                        membership_responses_model  = MembershipResponses.objects.get(club=club)
                        membership_responses_model.accepted.remove(removee)
                        membership_request_model    = MembershipRequest.objects.get(club=club,sender=removee)
                        membership_request_model.delete()
                        updateHistory   = ClubHistoryPerUser.objects.get(user=removee)
                        updateHistory.club_member.remove(club_called)
                        club_status = MemberStatus.objects.get(club=club,member=removee)
                        club_status.delete()
                        return Response({"Success Message":"Removed from club"})
                    else:
                        return Response({"Not Found":"Not a member"})
                else:
                    return Response({"Access Error":"Not the Owner or an Admin "})
        except:
            return Response({"Error":"Server Error"})

class ViewAllRequestsViewSet(APIView):
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    serializer_class        = MembershipRequestSerializer
    queryset                = Clubs.objects.all()
    
    def get(self,request,pk):
        
        try:
            club    = Clubs.objects.get(id=pk)
            if ((club.owner.id == request.user.id)or(Clubs.objects.filter(id=pk,admins=request.user.id))):
                _requests   = MembershipRequest.objects.filter(club=pk,is_active=True)
                serializer  = MembershipRequestSerializer(_requests,many=True)
                return Response({"requested members":serializer.data})
            else:
                return Response({"Your are not the owner or the admin of for the club."})
        except:
            return Response({"Not Found":"There is no club with the given 'ID'"})
        
         
class ClubAdminsViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def post(self,request,pk,user):
        
        try:
            club    = Clubs.objects.get(id=pk)
            account = Accounts.objects.get(id =user)
            if ClubAdmins.objects.filter(club=club,clubAdmins=account):
                return Response({"message":"Already a admin for the club."})
            else:
                if club.owner.id == request.user.id:
                    if Clubs.objects.filter(id=pk,members=user):
                        ClubAdmins.objects.get_or_create(club=club)
                        addAdmin = ClubAdmins.objects.get(club=pk)
                        if addAdmin.admin_count() >= 5:
                            return Response ({"Admin Limit": "Admin limit reached  ,remove an existing one."})
                        else:
                            getHistory = ClubHistoryPerUser.objects.get(user=user)
                            if getHistory.total_admin() >= 1:
                                return Response ({"Condition Error ":"User is already Admin for a different club."})
                            else:
                                addAdmin.clubAdmins.add(user)
                                club.admins.add(user)
                                getHistory.club_admin.add(club.id)
                                return Response({"Admin added"})       
                    else:
                        return Response({"Membership Error":"Only a member for the club can be added as admin."})
                else:
                    return Response({"Message":"You are not the owner for the club  inorder to add a admin."})  
        except:
            return Response({"Error":"Server Error"})
        
    def delete(self,request,pk,user):
        
        try:
            club    = Clubs.objects.get(id=pk)
            if club.owner.id == request.user.id:
                if Clubs.objects.filter(id=pk,admins=user):
                   
                    clubAdmin = ClubAdmins.objects.get(club=pk)
                    clubAdmin.clubAdmins.remove(user)
                    club.admins.remove(user)
                    getHistory = ClubHistoryPerUser.objects.get(user=user)
                    getHistory.club_admin.remove(pk)
                    return Response({"Status":"Removed from Admins"})
                else:
                    return Response({"Not an Admin"})
            else:  
                return Response({"Error":"Only owner of the club can remove admins."})
            
        except:
            return Response({"Error":"Server Error"})




class ExitFromClub(APIView):
     
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def post (self,request,club):
        
        try:
            club_called = Clubs.objects.get(id=club)
            if (request.user.id == club_called.owner.id):
                return Response({"Error":"Owner cannot exit the club."})
            else:
                if Clubs.objects.filter(id=club,members=request.user.id):
                    if Clubs.objects.filter(id=club,admins=request.user.id):
                        club_called.members.remove(request.user.id)
                        club_called.admins.remove(request.user.id)
                        membership_responses_model  = MembershipResponses.objects.get(club=club)
                        membership_responses_model.accepted.remove(request.user.id)
                        membership_request_model    = MembershipRequest.objects.get(club=club,sender=request.user.id)
                        membership_request_model.delete()
                        updateHistory   = ClubHistoryPerUser.objects.get(user=request.user.id)
                        updateHistory.club_member.remove(club_called)
                        club_status = MemberStatus.objects.get(club=club,member=request.user.id)
                        club_status.delete()
                        admin = ClubAdmins.objects.get(club=club)
                        admin.clubAdmins.remove(request.user.id)
                        return Response({"Success":"You left."})
                    else:
                        club_called.members.remove(request.user.id)
                        membership_responses_model  = MembershipResponses.objects.get(club=club)
                        membership_responses_model.accepted.remove(request.user.id)
                        membership_request_model    = MembershipRequest.objects.get(club=club,sender=request.user.id)
                        membership_request_model.delete()
                        updateHistory   = ClubHistoryPerUser.objects.get(user=request.user.id)
                        updateHistory.club_member.remove(club_called)
                        club_status = MemberStatus.objects.get(club=club,member=request.user.id)
                        club_status.delete()
                        return Response({"Success":"You left."})
                else:
                    return Response({"Error":"You are not a member for the club."})
        except:
            return Response({"Error":"Server Error"})
        
class ClubDeletion(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def delete(self,request):
        
        try:
            if Clubs.objects.filter(owner=request.user.id):
                getClub = Clubs.objects.get(owner=request.user.id)
                getClub.delete()
                return Response({"Success":"Your Club has been deleted."})
            else:
                return Response({"Error":"Only owner can delete the Club. "})
        except:
            return Response({"Error":"Server Error"})