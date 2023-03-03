from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import date
from multiselectfield import MultiSelectField

class AccountsManager(BaseUserManager):
    
    use_in_migrations = True
    
    def create_user(self,email,username,password):
        
        if not email:
            raise ValueError("Users must have an valid email address.")
        if not username :
            raise ValueError("User must have unique username.")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save()
        return user 
    

    def create_superuser(self,email,username,password):
        user =  self.create_user(
                                    email = self.normalize_email(email),
                                    username = username,
                                    password = password,
                            )
        
        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True
        user.save()
        return user
        


class Accounts(AbstractBaseUser):
    
    username        = models.CharField(max_length=30 ,unique = True)
    email           = models.EmailField(verbose_name='email', max_length=60 ,unique = True)
    date_joined     = models.DateTimeField(auto_now_add=True)
    hide_email      = models.BooleanField(default=True)
    
    is_superuser    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    
    objects = AccountsManager()
    
    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = ['username']
    
    def has_perm(self,perm,obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = "Accounts"
        
      
class Profile(models.Model):
    
    FOOTBALL    = "F"
    CRICKET     = "C"
    ALL     = "A"   
    GAME_CHOICE      = [
        (CRICKET, "Cricket"),
        (FOOTBALL, "Football"),
        (ALL, "All")
    ]
    
    
    DISTRICT_CHOICES = (
          ("AL", 'Alappuzha'),
          ("ER", 'Ernakulam'),
          ("ID", 'Idukki'),
          ("KN", 'Kannur'),
          ("KS", 'Kasaragod'),
          ("KL", 'Kollam'),
          ("KT", 'Kottayam'),
          ("KZ", 'Kozhikode'),
          ("MA", 'Malapuram'),
          ("PL", 'Palakkad'),
          ("PT", 'Pathanmthitta'),
          ("TV",'Thiruvanathapuram'),
          ("TS", 'Thirssur'),
          ("WA", 'Wayanad')
        )
    
    user                = models.ForeignKey(Accounts,on_delete = models.CASCADE)
    games               = models.CharField(choices=GAME_CHOICE,max_length= 5,default=ALL)
    
    name                = models.CharField(max_length=40,blank=False,null=True)
    
    DOB                 = models.DateField("Date in ( MM/DD/YYYY )",null= True,blank=False,
                                           auto_now=False,auto_now_add=False)
    profile_image       = models.ImageField(upload_to='profile_pictures',null=True,blank=True)
    bio                 = models.CharField(max_length =  500 ,blank = True)
    district            = models.CharField(max_length= 2,choices = DISTRICT_CHOICES,
                                           null= True,blank= False)
    
    def age(self):
        
        today  = date.today() 
        try:
            birthday = self.DOB.replace(year=today.year)
        except ValueError:
            birthday = self.DOB.replace(year=today.year,day=self.DOB.day-1)
    
        if birthday > today:
            return today.year - self.DOB.year - 1
        else :
            return today.year -self.DOB.year
        
  
    def __str__(self):
        return self.user.username
    
