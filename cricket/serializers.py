from rest_framework import  serializers
from .models import CricketPosts,PostFuntions,HostCricketTournaments


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = CricketPosts
        fields  = ('id','images','title','description','date','context')
        
class PostViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = CricketPosts
        fields  = ('id','images','title','description','date','context','nameUser')
        
class UpadateDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = CricketPosts
        fields  = ('images','title','description','context')
        
        
class PostFuntionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = PostFuntions
        fields  = ('likes','dislike','report','number_of_likes','number_of_dislikes')  
        
           
class HostTournamentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   = HostCricketTournaments
        fields  = ('tournament_name','venue','district','banner',
                   'description','date','limit_participants','contact',
                   'end_registration')
        
        

        
         