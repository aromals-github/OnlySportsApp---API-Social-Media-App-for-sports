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
    name          = models.CharField(max_length=90,null=True,blank=True)
    games         = models.CharField(max_length=2,choices=GAME_CHOICE,blank=True)
    members       = models.ManyToManyField(Accounts,related_name="members",blank=True,
                                                error_messages={'max-limit':'max of 60 members'}) 
    logo          = models.ImageField(upload_to='clubs logos',blank=True,null=True)
    district      = models.CharField(max_length=30,choices=DISTRICT_CHOICES,null=True,blank=True)
    owner         = models.ForeignKey(Accounts,on_delete=models.CASCADE,blank=True)
    class Meta:
        verbose_name_plural = "Clubs"  
      
def changes(sender,**kwargs):
    if kwargs['instance'].members.count() > 60:
        raise ValidationError('You cant have more than 30 members in a club')       
m2m_changed.connect(changes,sender  = Clubs.members.through)


class ClubAdmins(models.Model):
    
    club        = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    clubAdmins  = models.ManyToManyField(Accounts,related_name="Club_Admins",blank=True)
    
    class Meta:
        verbose_name_plural = "Club Admins"
    
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
    

def changes_Admin(sender,**kwargs):
    if kwargs['instance'].clubAdmins.count() > 5:
        raise ValidationError('You cant have more than 5 members as admins')       
m2m_changed.connect(changes_Admin,sender  = ClubAdmins.clubAdmins.through)
  
    