from rest_framework import  serializers
from .models import *


class HostTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = HostFootballTournaments
        fields  = ('tournament_name','venue','district','banner',
                   'description','date','limit_participants','contact',
                   'end_registration')
          
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = HostFootballTournaments
        fields  = ('tournament_name','venue','district','banner',
                   'description','date','limit_participants','contact',
                   'end_registration')

class TournamentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model   = HostFootballTournaments
        fields  = ('id','tournament_name','venue','district','banner',
                   'description','date','limit_participants','contact',
                   'end_registration','date_added','registered_teams')
        