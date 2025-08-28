from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'skill_level']
    list_filter = ['skill_level']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']