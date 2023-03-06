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



class StatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MemberStatus
        fields = ('club','club_name','member','member_name','status')
        
        
class CricketTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClubCricketMembers
        fields = ('tournament_Name','player_name','players_count',)
        


class FootballTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClubCricketMembers
        fields = ('tournament_Name','player_name','players_count',)