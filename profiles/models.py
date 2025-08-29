from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import os

# Create your models here.
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
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        default='../default_profile_qohqce'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class CoachProfile(models.Model):
    CERTIFICATION_LEVELS = [
        ('level1', 'Level 1 - Assistant Coach'),
        ('level2', 'Level 2 - Head Coach'),
        ('level3', 'Level 3 - Senior Coach'),
        ('level4', 'Level 4 - Master Coach'),
    ]
    
    SPECIALTIES = [
        ('technique', 'Technique Development'),
        ('strategy', 'Game Strategy'),
        ('fitness', 'Physical Conditioning'),
        ('mental', 'Mental Game'),
        ('youth', 'Youth Development'),
        ('performance', 'Performance Coaching'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    certification_level = models.CharField(max_length=10, choices=CERTIFICATION_LEVELS)
    specialties = models.CharField(max_length=100, help_text="Comma-separated list of coaching specialties")
    years_experience = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(70)]
    )
    hourly_rate = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    profile_image = models.ImageField(
        upload_to='coach_profiles/',
        blank=True,
        null=True,
        default='../default_coach_profile'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)
    
    def get_specialties_list(self):
        return [specialty.strip() for specialty in self.specialties.split(',')]
    
    def profile_image_url(self):
        """
        Return the URL for the coach's profile image or a default if none exists
        """
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return '/static/images/default_coach_profile.png'
    
    def __str__(self):
        return f"Coach: {self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = "Coach Profile"
        verbose_name_plural = "Coach Profiles"


class CoachAvailability(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.coach.user.first_name}'s {self.get_day_of_week_display()} Availability"


class CoachReview(models.Model):
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name='reviews')
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.rating} star review for {self.coach.user.first_name} by {self.player.user.first_name}"