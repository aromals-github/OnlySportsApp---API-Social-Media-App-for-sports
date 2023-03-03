from rest_framework import  serializers
from .models import *
from clubs.models import Clubs


class AllClubMemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Clubs
        fields  = ('members','name_members')

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Accounts
        fields  = ('username','id')
