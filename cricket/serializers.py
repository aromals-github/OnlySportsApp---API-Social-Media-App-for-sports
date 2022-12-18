from rest_framework import  serializers
from .models import CricketPosts,PostFuntions


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = CricketPosts
        fields  = ('id','images','title','description','date','context')
        
class UpadateDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = CricketPosts
        fields  = ('images','title','description','context')
        
        
class PostFuntionSeriaizer(serializers.ModelSerializer):
    
    class Meta:
        model   = PostFuntions
        fields  = ('id','post_id','likes','dislike','report')   
        
        