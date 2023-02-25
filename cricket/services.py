from users.models import Profile

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
        