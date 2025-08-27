from django.db import models
from profiles.models import PlayerProfile
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class TrainingSession(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='training_sessions')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    focus_area = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    intensity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rate intensity from 1 (low) to 10 (high)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
    
    def duration(self):
        from datetime import datetime
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        return (end - start).total_seconds() / 3600  # Return hours
    
    def __str__(self):
        return f"{self.player.user.get_full_name()} - {self.date} {self.focus_area}"