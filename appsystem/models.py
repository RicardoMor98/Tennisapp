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