from django.contrib import admin
from .models import PlayerProfile

# Register your models here.
@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_level']
    list_filter = ['skill_level']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']