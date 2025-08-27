from django.db import models
from django.contrib.auth.models import User
from profiles.models import PlayerProfile

# Create your models here.
class Tournament(models.Model):
    SURFACE_TYPES = [
        ('clay', 'Clay'),
        ('grass', 'Grass'),
        ('hard', 'Hard Court'),
        ('carpet', 'Carpet'),
    ]
    
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    surface = models.CharField(max_length=10, choices=SURFACE_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournaments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class TournamentRegistration(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='tournament_registrations')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    seed = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ['player', 'tournament']
    
    def __str__(self):
        return f"{self.player.user.get_full_name()} - {self.tournament.name}"