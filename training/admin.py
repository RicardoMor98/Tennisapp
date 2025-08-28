from django.contrib import admin
from .models import TrainingSession, TennisCourt

# Register your models here.
@admin.register(TennisCourt)
class TennisCourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'surface_type', 'is_indoor']
    list_filter = ['surface_type', 'is_indoor']
    search_fields = ['name', 'location']

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'coach', 'court', 'date_time', 'skill_level', 'price']
    list_filter = ['skill_level', 'court', 'date_time']
    search_fields = ['title', 'coach__username', 'court__name']
    date_hierarchy = 'date_time'