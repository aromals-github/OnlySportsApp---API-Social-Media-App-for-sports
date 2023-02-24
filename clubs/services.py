from clubs.models import *
from users.models import *


def clubRepo(request):
    user_ID = request.user.id    
    if ClubHistoryPerUser.objects.filter(user =request.user.id,owner=True):
        return(0)
        
    else :
        getHistory = ClubHistoryPerUser.objects.get(user=request.user.id)
        print (getHistory.total_admin)
        if getHistory.total_admin() > 0 or getHistory.total_membership() > 0:
            return (0)
        else:
            return (1)      

def updateClubHistory(request):
    ClubHistoryPerUser.objects.filter(user=request.user.id).update(owner=True)     
    
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
        
