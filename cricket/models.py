from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Accounts

class CricketPosts(models.Model):
    
    user                = models.ForeignKey(Accounts,on_delete = models.CASCADE)
    images              = models.ImageField(upload_to= "cricket_posts",blank= True,null= True)
    title               = models.CharField(max_length= 80,blank= True,null= True)
    description         = models.TextField(max_length= 500,blank= False)
    date                = models.DateTimeField(auto_now_add = True, null=True,blank=True)
    
  
    
    class Meta:
        verbose_name_plural = "cricket posts"
        verbose_name        = 'cricket post'
        
class Post_Funtions(models.Model):
    post_id             = models.OneToOneField(CricketPosts,on_delete= models.CASCADE)
    # like              = 