from rest_framework import  serializers
from .models import CricketPosts


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = CricketPosts
        fields  = ('id','images','title','description','date')