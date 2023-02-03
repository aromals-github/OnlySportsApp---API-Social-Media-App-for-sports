from rest_framework import serializers
from .models import *



class ClubSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = Clubs
        fields  = ('name','district','games','logos')