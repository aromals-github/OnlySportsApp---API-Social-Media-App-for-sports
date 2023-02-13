from clubs.models import Clubs
from users.models import Accounts,Profile

def clubRepo(request):
    user_ID = request.user.id    
    if Clubs.objects.filter(owner=user_ID):
        return(0) #If user exist return 1 means a clubs exist for this user as owner.
    else :
        return (1)# No clubs exists for this user thus a new club can be created
    



