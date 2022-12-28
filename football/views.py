from rest_framework import status
from rest_framework.response import Response

from users.models import Accounts,Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from.models import FootballPosts
from .serializers import FootballPostSerializer
from rest_framework.views import APIView

class FootballPostViewSet(APIView):
    
    queryset                = FootballPosts.objects.all()
    serializer_class        = FootballPostSerializer
    authentication_classes  = (TokenAuthentication,)
    permission_classes      = (IsAuthenticated,)
    
    
    def post(self,request,*args,**kwargs):
        
        try:
            user_logged     = request.user
            user_id         = user_logged.id

            if Profile.objects.get(user = user_id):
                profile= Profile.objects.get(user = user_id)
                
                if (('F' in profile.games ) and 
                    ('F' in request.data['context'])) or ('G' in profile.games):
                   
                    user_id_logged = Accounts.objects.get(id = user_id)
                    user = FootballPosts.objects.create(user = user_id_logged)
                    serializer = FootballPostSerializer(user,data = request.data)
                    
                    if serializer.is_valid():
                        serializer.save()
                        
                        return Response({'data': serializer.data},status = 
                                        status.HTTP_201_CREATED)
                    else:
                        return Response({'errors':serializer.errors},status = 
                                        status.HTTP_400_BAD_REQUEST)
                else:
                    response =({'message': 
                        "You can't create a post related to cricket,with your current profile "})
                    return Response(response,status = status.HTTP_403_FORBIDDEN) 
            
        except:
            
            response = ({'message': 'You are not logged in or you dont have an profile'})
            return Response(status = status.HTTP_206_PARTIAL_CONTENT)
        
        