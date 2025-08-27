from django.db import models  
from django.contrib.auth.models import User  
from django.core.validators import MinValueValidator, MaxValueValidator  
import os  


# Create your models here.
def user_image_path(instance, filename):  
    # Upload to media/user_<id>/profile_<filename>  
    return f'user_{instance.user.id}/profile_{filename}'

class PlayerProfile(models.Model):  
    SKILL_LEVELS = [  
        ('beginner', 'Beginner'),  
        ('intermediate', 'Intermediate'),  
        ('advanced', 'Advanced'),  
        ('competition', 'Competition'),  
    ]  

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    date_of_birth = models.DateField()  
    skill_level = models.CharField(max_length=12, choices=SKILL_LEVELS)  
    profile_image = models.ImageField(upload_to=user_image_path, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
  
    def age(self):  
        import datetime  
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)  
      
    def __str__(self):  
        return f"{self.user.first_name} {self.user.last_name}"

class TrainingSession(models.Model):  
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)  
    date = models.DateField()  
    start_time = models.TimeField()  
    end_time = models.TimeField()  
    focus_area = models.CharField(max_length=100)  
    notes = models.TextField(blank=True)  
    intensity = models.IntegerField(  
        validators=[MinValueValidator(1), MaxValueValidator(10)],  
        help_text="Rate intensity from 1 (low) to 10 (high)"  
    )  
      
    class Meta:  
        ordering = ['-date', '-start_time']  
  
    def duration(self):  
        from datetime import datetime  
        start = datetime.combine(self.date, self.start_time)  
        end = datetime.combine(self.date, self.end_time)  
        return (end - start).total_seconds() / 3600  # Return hours

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
    participants = models.ManyToManyField(PlayerProfile, through='TournamentRegistration')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class TournamentRegistration(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    seed = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ['player', 'tournament']