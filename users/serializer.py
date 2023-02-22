from rest_framework import serializers
from .models import Accounts,Profile
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model           = Accounts
        fields          = ('email','username','password')
        extra_kwargs    = {'passwords': {'write_only':True, 'required':True}}
 
        
    def create(self,validated_data):
        user            = Accounts.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta :
        model           = Profile
        fields          = ('games','profile_image','DOB','bio','name','district')      
        
        
class TokenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model           = Token
        fields          = ('key', )