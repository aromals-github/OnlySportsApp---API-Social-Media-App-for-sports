from django.db import models
from users.models import Accounts

class CricketPosts(models.Model):
    
    
    CRICKET     = "C"
    GENERAL     = "G"  
    GAME_CHOICE      = [
        (CRICKET, "Cricket"),
        (GENERAL, "General"),
    ]
    
    user                = models.ForeignKey(Accounts,on_delete = models.CASCADE)
    images              = models.ImageField(upload_to = "cricket_posts",blank = True,null = True)
    title               = models.CharField(max_length = 80,blank = True,null = True)
    description         = models.TextField(max_length = 500,blank = False)
    date                = models.DateTimeField(auto_now_add = True, null = True,blank = True) 
    context             = models.CharField(max_length=2,choices = GAME_CHOICE,blank=True
                                           ,null=True)
    
    ''' Here the context has to changed to blank = False and null = False
        Post should always contain a handle which is the 
        context '''
    class Meta:
        verbose_name_plural = "cricket posts"
        verbose_name        = 'cricket post'
        
    def nameUser(self):
        user = self.user
        userPost = Accounts.objects.get(email=user)
        return (userPost.username)
class PostFuntions(models.Model):
    
    DEFAULT = 0  
    REASON1 = 1
    REASON2 = 2
    REASON3 = 3
    REASON4 = 4

    REPORT_REASON = [
        (DEFAULT,"NONE"),
        (REASON1, "This post is not related to cricket"),
        (REASON2, "Content of the this particular post is abusive"),
        (REASON3, "Sexual Content ") ,
        (REASON4, "Others")
    ]
    
    post_id             = models.OneToOneField(CricketPosts,on_delete = models.CASCADE)
    likes               = models.ManyToManyField(Accounts,related_name ='likes',blank=True)
    dislike             = models.ManyToManyField(Accounts,related_name='dislike',blank=True)
    report              = models.IntegerField(
                                           choices = REPORT_REASON,
                                           default = DEFAULT
                                           )
    class Meta:
        verbose_name_plural = "post funtions"
      
      
    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_dislikes(self):
        return self.dislike.count()
    