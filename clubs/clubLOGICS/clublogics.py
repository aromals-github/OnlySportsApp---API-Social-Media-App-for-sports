from clubs.models import *
from users.models import Accounts,Profile

def clubRepo(request):
    user_ID = request.user.id    
    if Clubs.objects.filter(owner=user_ID):
        return(0) #If user exist return 1 means a clubs exist for this user as owner.
    else :
        return (1)# No clubs exists for this user thus a new club can be created
    
def membershipList(request,club):
    user = request.user.id
    
    if MembershipResponses.objects.filter(club=club):
        request_club = Clubs.objects.get(id=club)
        store = MembershipResponses.objects.get(club=request_club)
        if request_club.owner.id == user:
            return(False)
        else:
            store.waiting.add(user)
            return True
    else:
        request_club = Clubs.objects.get(id=club)
        store = MembershipResponses.objects.create(club=request_club)
        if request_club.owner.id == user:
            return(False)
        else:
            store.waiting.add(user)
            return True
        
        
        

