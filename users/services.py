from .models import *
from clubs.models import *


def createClubHistory(request):
    
    account = Accounts.objects.get(id = request.user.id)
    ClubHistoryPerUser.objects.create(user=account)