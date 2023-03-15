from rest_framework import  serializers
from .models import *


class HostTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = HostCricketTournaments
        fields  = ('tournament_name','venue','district','banner',
                   'description','date','limit_participants','contact',
                   'end_registration')
          
class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = HostCricketTournaments
        fields  = ('tournament_name','venue','district','banner',
                   'description','date','limit_participants','contact',
                   'end_registration')

class TournamentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model   = HostCricketTournaments
        fields  = ('id','tournament_name','venue','district','banner',
                   'description','date','limit_participants','contact',
                   'end_registration','date_added','registered_teams')
        
        
        
class Serializer_One(serializers.ModelSerializer):
    
    class Meta:
        model   = HostCricketTournaments
        fields  = ('tournament_name','venue','district','banner',
                   'description','date','contact',
                   'end_registration','id','registered')
        

        
class Serializer_Two(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Participants
        fields = ('count_participants','participants')

class Serializer_Three(serializers.ModelSerializer):
    team_won = serializers.StringRelatedField()
    
    class Meta:
        model = TournamentResult
        fields = ('team_won','date_added')

class CombinedSerializer(serializers.Serializer):
    
    tournament   = Serializer_One(many=False)
    participants = Serializer_Two(many=False)
    result       = Serializer_Three()
    
    def to_representation(self, instance):
        representation  = super().to_representation(instance)
        return {
            'Tournament Information'    : representation['tournament'],
            'Participants'              : representation['participants'],
            'Result'                    : representation['result'],
        }