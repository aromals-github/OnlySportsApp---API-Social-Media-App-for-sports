from django.db import models
from django.utils.translation import gettext_lazy as _


class CricketPosts(models.Model):
    
    # user              = ForeginKey(Users,on_delete = models.CASCADE)
    # handle            = slection ----- needs to be done
    images              = models.ImageField(upload_to= "cricket_posts",blank= True,null= True)
    title               = models.CharField(max_length= 80,blank= True,null= True)
    description         = models.TextField(max_length= 500,blank= False)
    
  
    
    class Meta:
        verbose_name_plural = "cricket posts"