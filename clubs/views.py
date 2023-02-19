
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from clubs.clubLOGICS.clublogics import *
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
                if verifyUser == 1:
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
            return Response ({"Profile  doesn't match with selected game."})
        
        
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
        try:
            if pk != 0:
                if Clubs.objects.filter(id=pk):
                    club = Clubs.objects.get(id=pk)
                    serializer = ClubInfoViewSerializer(club)
                    return Response({"club details": serializer.data})
                else:
                    return Response({"No club exists"})
            
            elif pk==0:
                AllClubs = Clubs.objects.all()
                serializer = ClubInfoViewSerializer(AllClubs,many=True)
                return Response({"all clubs":serializer.data})
        except:
            return Response({"Unknown error"})
        
class ClubMembershipViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = MembershipRequest.objects.all()
    
    ''' ** MEMBERSHIP **
        -> Users can cancel the request at any time .
        -> 3 Possible Responses
    '''
    def post(self,request,pk,action): 
        
        try:
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
                                return Response({"Status":"You are already a member of the club"})
                            else:
                                if list_created == False:
                                    return Response({"Owner is assigned to all roles in club by default."})
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
                            return Response ({"Cancelled"})
                        else:
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                    
                    else:
                        return Response({"error":"URL-/<int:action> || value should be 1 (Send Request) or 0 (Cancel Request)."})
                
        except:
             return Response({"ERROR WITH SELECTED CLUB":"This club is either terminated or never existed."})   
         
          

class ClubMembershipResponse(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    queryset                = Clubs.objects.all()
    
    def post(self,request,pk,user,action):
        try:
            if MembershipResponses.objects.get(club=pk):
                club = Clubs.objects.get(id=pk)
                if ((club.owner.id == request.user.id)or(Clubs.objects.filter(id=pk,admins=request.user.id))) :
                    account = Accounts.objects.get(id=user)
                    if action == 1:
                        
                        response_model_accepted = MembershipResponses.objects.get(club=pk)
                        response_model_accepted.waiting.remove(user)
                        response_model_accepted.accepted.add(user)
                        
                        if MembershipRequest.objects.get(club=pk,sender=account,is_active=True):
                            membership_model_accepted = MembershipRequest.objects.get(club=pk,sender=account,is_active=True)
                            membership_model_accepted.delete()
                            club_requested = Clubs.objects.get(id=pk)
                            new_instance_accepted = MembershipRequest(club=club_requested,sender=account,is_active=False)
                            new_instance_accepted.save()                               
                        club_model_accepted = Clubs.objects.get(id=pk)
                        club_model_accepted.members.add(user)
                        return Response({"Status":"Accepted"})
                    
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
                        return Response({"Invalid Response, || URL "})
                else:
                    return Response({"Only owner and club admins can accept and decline memebership requests."})
            else:
                return Response({"Club does not exists."})
        except:
            return Response({"Error": "No Request to Respond or Invalid action"})

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
                        return Response({"Success Message":"Removed from club"})
                    else:
                        return Response({"Not Found":"Not a member"})
                else:
                    return Response({"Access Error":"Not the Owner or an Admin "})
        except:
            return Response({"Error"})

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
            return Response({"There is no club with the given 'ID'"})
        
         
class ClubAdminsViewSet(APIView):
    
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    def post(self,request,pk,user):
        
        try:
            club    = Clubs.objects.get(id=pk)
            if club.owner.id == request.user.id:
                if Clubs.objects.filter(id=pk,members=user):
                    ClubAdmins.objects.get_or_create(club=club)
                    addAdmin = ClubAdmins.objects.get(club=pk)
                    print(addAdmin.admin_count())
                    if addAdmin.admin_count() >= 5:
                        return Response ({"Admin Limit": "Admin limit reached to add new admin ,remove an existing one."})
                    else:
                        addAdmin.clubAdmins.add(user)
                        club.admins.add(user)
                        return Response({"Admin added"})       
                else:
                    return Response({"Membership":"Not an member for the club to be an admin."})
            else:
                return Response({"You are not the owner for the club  inorder to add or remove a admin."})
        except:
            return Response({"Error"})
        
    def delete(self,request,pk,user):
        
        try:
            club    = Clubs.objects.get(id=pk)
            if club.owner.id == request.user.id:
                if Clubs.objects.filter(id=pk,admins=user):
                    clubAdmin = ClubAdmins.objects.get(club=pk)
                    clubAdmin.clubAdmins.remove(user)
                    club.admins.remove(user)
                    return Response({"Status":"Removed from Admins"})
                else:
                    return Response({"Not an Admin"})
            else:  
                return Response({"Error":"Only owner of the club can remove admins."})
            
        except:
            return Response({"Club not found or error in loading admins"})
        