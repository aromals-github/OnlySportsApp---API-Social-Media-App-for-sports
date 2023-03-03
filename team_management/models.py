from django.db import models
from clubs.models import *
from cricket.models import HostCricketTournaments
from football.models import HostFootballTournaments
from users.models import Accounts



class MemberStatus(models.Model):
    club            = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    member          = models.ForeignKey(Accounts,on_delete=models.CASCADE,blank=False)
    status          = models.BooleanField(default=True)
    
    
    class Meta:
        verbose_name_plural = " MEMBER STATUS"

    def __str__(self):
        return self.member.username


class MemberTournamentStatus(models.Model):
    club            = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    member          = models.ForeignKey(Accounts,on_delete=models.CASCADE,blank=False)
    status          = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Member Status Per Tournament"
    
    def __str__(self):
        return (self.member.username)
    
class ClubCricketMembers(models.Model):
    
    club            = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    players         = models.ManyToManyField(Accounts,related_name="cricket_players",blank=True)
    tournament      = models.ForeignKey(HostCricketTournaments,on_delete=models.CASCADE,blank=False)
    
    class Meta:
        verbose_name_plural = "Cricket Members"
        
    def __str__(self):
        return self.club.name


class ClubFootballMembers(models.Model):
    
    club            = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=True)
    players         = models.ManyToManyField(Accounts,related_name="football_players",blank=True)
    tournament      = models.ForeignKey(HostFootballTournaments,on_delete=models.CASCADE,blank=False)
    
    class Meta:
        verbose_name_plural = "Football Members"
        
    def __str__(self):
        return self.club.name


class ClubRegisteredCricketTournament(models.Model):
    
    tournament      = models.ManyToManyField(HostCricketTournaments,blank=True)
    club            = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=True)
    
    class Meta:
        verbose_name_plural = "Registered Tournaments Per Club"
        
    def __str__(self):
        return self.club.name



class ClubRegisteredFootballTournament(models.Model):
    
    tournament      = models.ManyToManyField(HostCricketTournaments,blank=True)
    club            = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=True)
    
    class Meta:
        verbose_name_plural = "Registered Tournaments Per Club"
        
    def __str__(self):
        return self.club.name



class Club_Games_History(models.Model):
    
    club                            = models.ForeignKey(Clubs,on_delete=models.CASCADE,blank=False)
    
    cricket_registed                = models.ManyToManyField(HostCricketTournaments,related_name='cricket_registered',blank=True)
    participated_cricket            = models.ManyToManyField(HostCricketTournaments,related_name='cricket_participated',blank=True)
    cricket_tournaments_won         = models.ManyToManyField(HostCricketTournaments,related_name='cricket_won',blank=True)
    
    football_registered            = models.ManyToManyField(HostFootballTournaments,related_name='football_registered',blank=True)
    participated_football           = models.ManyToManyField(HostFootballTournaments,related_name='football_participated',blank=True)
    football_tournaments_won        = models.ManyToManyField(HostFootballTournaments,related_name='football_won',blank=True)
    
    class Meta:
        verbose_name_plural = "Club History"
    
    def registered_cricket(self):
        return self.cricket_tournaments_registed.count()
    
    def registered_football(self):
        return self.football__registered.count()
    
    def cricket_won(self):
        return self.cricket_tournaments_won.count()
    
    def football_won(self):
        return self.football_tournaments_won.count()
    
    def __str__(self):
        return self.club.name