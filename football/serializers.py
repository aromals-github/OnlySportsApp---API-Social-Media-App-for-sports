from .models import FootballPosts,PostFuntions
from rest_framework import serializers


class FootballPostSerializer(serializers.ModelSerializer):
    
  class Meta:
        model   = FootballPosts
        fields  = ('id','images','title','description','date','context')