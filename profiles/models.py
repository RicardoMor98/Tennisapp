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