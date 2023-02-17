from rest_framework import serializers
from .models import *



class ClubSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Clubs
        fields  = ('name','district','games','logo')
        
        
class ClubUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Clubs
        fields  = ('name','district','games','logo')
        
class ClubsAdminSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = ClubAdmins
        fields  = ('club',)
        
class ClubInfoViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Clubs
        fields  = ('name','owner','games','logo','district')


class MembershipRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = MembershipRequest
        fields  = ('sender','timestamp','sender_name')   