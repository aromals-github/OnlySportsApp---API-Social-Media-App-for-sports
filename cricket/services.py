from users.models import Profile
from .models import *
def verify_user(request):
    
    user        = request.user.id
    p = Profile.objects.filter(user=user)
    if not p:
        return(4)
    else:
        profile = Profile.objects.get(user=user)
        if (('C' in profile.games) or ('A' in profile.games )):
            age         = profile.age()
            if age>=18:
                return (True)
            else :
                return(2)     
        else:
            return (False)

def report_action(pk):
    getReport = Tournament_Reports.objects.get(tournament=pk)
    if getReport.count_reporters() >15 :
        Tournament_Notifications.objects.update(tournament=pk,verified = False,reported =True)
    else:
        pass 
    
         
         
         
