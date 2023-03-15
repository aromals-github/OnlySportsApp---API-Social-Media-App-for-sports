from django.db import models
from users.models import Accounts
from clubs.models import Clubs

class HostFootballTournaments(models.Model):
    
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

    host               = models.ForeignKey(Accounts,on_delete = models.CASCADE,blank=False,null=False)
    tournament_name    = models.CharField(max_length = 70,blank = True,null = True)
    banner             = models.ImageField(upload_to='FootballTournaments',blank = True, null=True)
    district           = models.CharField(max_length= 2,choices = DISTRICT_CHOICES,null= True,blank= True)
    venue              = models.CharField(max_length = 70,blank = True,null = True)
    date_added         = models.DateTimeField(auto_now_add = True) 
    description        = models.TextField(max_length=1000,null=True,blank=True) 
    date               = models.DateField(blank=False,null=True)
    limit_participants = models.IntegerField(blank=True,null=True)
    contact            = models.CharField(max_length=600,null=True,blank=True)
    end_registration   = models.DateField(blank=True,null=True)
    registered_teams   = models.ManyToManyField(Clubs,related_name="RegisteredForFootball",blank=True)

    class Meta:
        verbose_name_plural = "Football Tournaments"
        verbose_name        = 'Football Tournament'
        
    def __str__(self):
        return self.tournament_name


class Tournament_Notifications(models.Model):
    
    tournament      = models.ForeignKey(HostFootballTournaments,on_delete=models.CASCADE,blank=False)
    verified        = models.BooleanField(default=True)
    cancelled       = models.BooleanField(default=False)
    reported        = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Notifications"
        
    def __str__(self):
        return self.tournament.tournament_name
     


class Tournament_Reports(models.Model):
    
    tournament      = models.ForeignKey(HostFootballTournaments,on_delete=models.CASCADE,blank=True)
    reporters       = models.ManyToManyField(Accounts,related_name="reporters_Football",blank=True)
    
    def count_reporters(self):
        return self.reporters.count()
    
    class Meta:
        verbose_name_plural ="Reports"
        
    def __str__(self):
        return self.tournament.tournament_name

       
class Resgister_Tournaments(models.Model):
    
    tournament = models.ForeignKey(HostFootballTournaments,on_delete=models.DO_NOTHING)
    registered = models.ManyToManyField(Clubs,related_name="registered_Football",blank=True)
    
    
    class Meta:
        verbose_name_plural = "Registered Teams"
        
    def __str__(self):
        return self.tournament.tournament_name
    
    def count_teams(self):
        return self.registered.count()


class Participants(models.Model):
    
    tournament = models.ForeignKey(HostFootballTournaments,on_delete=models.DO_NOTHING)
    participants = models.ManyToManyField(Clubs,related_name="participants_football",blank=True)
    
    
    class Meta:
        verbose_name_plural = "Participated Teams Football"
        
    def __str__(self):
        return self.tournament.tournament_name
    
    def count_participants(self):
        return self.participants.count()
    
    def participated(self):
        return [team.name for team in self.participants.all()]
    
    
class FootballTournamentResult(models.Model):
    
    tournament  = models.ForeignKey(HostFootballTournaments,on_delete=models.CASCADE,blank=False)
    date_added  = models.DateTimeField(auto_now_add=True)
    won         = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    
    class Meta:
        verbose_name_plural = "Football Tounament Results"
        
    def __str__(self):
        return self.tournament.tournament_name
    
