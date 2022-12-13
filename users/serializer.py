from rest_framework import serializers
from .models import Accounts,Profile
from rest_framework.authtoken.models import Token

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model           = Accounts
        fields          = ('id','username','password','name','email')
        extra_kwargs    = {'passwords': {'write_only':True, 'required':True}}
        
    def create(self,validated_data):
        users     = Accounts.objects.create_user(**validated_data)
        Token.objects.create(user=users)
        return users
    
    
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta :
        model           = Profile
        fields          = ('user','games','profile_image','DOB','age')      