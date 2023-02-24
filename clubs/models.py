from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from users.models import Accounts
from multiselectfield import MultiSelectField

class Clubs(models.Model):
    
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
       
    FOOTBALL    = "F"
    CRICKET     = "C"
    ALL         = "A"   
    GAME_CHOICE      = [
        (CRICKET, "Cricket"),
        (FOOTBALL, "Football"),
        (ALL,"All")
    ]
    name          = models.CharField(max_length=90,null=False,blank=False)
    games         = models.CharField(max_length=2,choices=GAME_CHOICE,blank=False)
    members       = models.ManyToManyField(Accounts,related_name="members",blank=True,
                                                error_messages={'max-limit':'max of 60 members'}) 
    logo          = models.ImageField(upload_to='clubs logos',blank=True,null=True)
    district      = models.CharField(max_length=30,choices=DISTRICT_CHOICES,null=True,blank=False)
    owner         = models.ForeignKey(Accounts,on_delete=models.CASCADE,blank=True)
    admins        = models.ManyToManyField(Accounts,related_name="admins",blank=True)
    
    class Meta:
        verbose_name_plural = "Clubs"  
    
    def __str__(self):
        return self.name
      
def changes(sender,**kwargs):
    if kwargs['instance'].members.count() > 60:
        raise ValidationError('You cant have more than 30 members in a club')       
m2m_changed.connect(changes,sender  = Clubs.members.through)



class MembershipRequest(models.Model):
    
    '''changes needs to be done in production
    
        1. sender should not be null 
        
    '''
    
    club        = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    sender      = models.ForeignKey(Accounts,blank=True,null=True,on_delete=models.CASCADE) 
    is_active   = models.BooleanField(blank=True,null=False,default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Membership Requests"
    
    def sender_name(self):
        account = Accounts.objects.get(id=self.sender.id)
        return (account.username)
        
    def name(self):
        Club = Clubs.objects.get(id=self.club.id)  
        return (Club.name)
    
    def owner(self):
        Club = Clubs.objects.get(id=self.club.id)
        return(Club.owner)

    def __str__(self):
        return self.club.name

class MembershipResponses(models.Model):
    
    club        = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=True)
    accepted    = models.ManyToManyField(Accounts,related_name="accepted",blank=True)
    blocked     = models.ManyToManyField(Accounts,related_name="blocked",blank=True)
    waiting     = models.ManyToManyField(Accounts,related_name="waiting",blank=True)
    
    def __str__(self):
        return self.club.name
    class Meta:
        verbose_name_plural = "Club Membership Responses"
         
        
class ClubAdmins(models.Model):
    
    club        = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    clubAdmins  = models.ManyToManyField(Accounts,related_name="Club_Admins",blank=True)
    time_stamp  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    class Meta:
        verbose_name_plural = "Club and Admins"
        
    def __str__(self):
        return self.club.name
    
    def club_name(self):
        
        getClub = self.club.id
        Club = Clubs.objects.get(id=getClub)
        name = Club.name   
        return (name)
    
    
    def owner(self):
        
        getClub = self.club.id
        Club = Clubs.objects.get(id=getClub)
        owner = Club.owner
        return(owner)
    
    def admin_count(self):
        
        count = self.clubAdmins.count()
        return(count)
    

def changes_Admin(sender,**kwargs):
    if kwargs['instance'].clubAdmins.count() > 5:
        raise ValidationError('You cant have more than 5 members as admins')       
m2m_changed.connect(changes_Admin,sender  = ClubAdmins.clubAdmins.through)
  


class ClubHistoryPerUser(models.Model):
    
    user                = models.ForeignKey(Accounts,on_delete=models.CASCADE,blank=True,null=True)        
    owner               = models.BooleanField(default=False)
    club_member         = models.ManyToManyField("clubs.Clubs",related_name="member",blank=True)
    club_admin          = models.ManyToManyField("clubs.Clubs",related_name="admin",blank=True)
    
    class Meta:
        verbose_name_plural = "Club History of Users"
        
    def __str__(self):
        return self.user.username

    
    def total_membership(self):
        return self.club_member.count()
    
    def total_admin(self):
        return self.club_admin.count()