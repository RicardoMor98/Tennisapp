from django.contrib import admin
from .models import TennisCourt, TrainingSession, Tournament, Booking, UserProfile

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

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'entry_fee', 'max_participants']
    list_filter = ['start_date']
    search_fields = ['title']
    date_hierarchy = 'start_date'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_event', 'booked_at', 'status']
    list_filter = ['status', 'booked_at']
    search_fields = ['user__username', 'session__title', 'tournament__title']
    
    def get_event(self, obj):
        if obj.session:
            return obj.session.title
        elif obj.tournament:
            return obj.tournament.title
        return "No event"
    get_event.short_description = 'Event'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_level', 'phone_number']
    list_filter = ['skill_level']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']