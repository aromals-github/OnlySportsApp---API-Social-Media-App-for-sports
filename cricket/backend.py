from .models import PostFuntions,CricketPosts
from .serializers import PostFuntionSerializer


def createPostFuntions():
   
    post_called     = CricketPosts.objects.latest('id')
    post_save       = PostFuntions.objects.create(post_id=post_called)
    serializer      = PostFuntionSerializer(post_save)
    return (serializer)