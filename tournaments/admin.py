from django.contrib import admin
from .models import Tournament, TournamentRegistration

# Register your models here.
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "start_date", "end_date", "surface", "created_by", "created_at"]
    list_filter = ['start_date']
    search_fields = ['title']
    date_hierarchy = 'start_date'

@admin.register(TournamentRegistration)
class TournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ("player", "tournament", "registration_date")
    list_filter = ("tournament", "registration_date")
    search_fields = ("player__user__username", "tournament__name")
    
    def get_event(self, obj):
        if hasattr(obj, 'session') and obj.session:
            return obj.session.title
        elif hasattr(obj, 'tournament') and obj.tournament:
            return obj.tournament.title
        return "No event"
    get_event.short_description = 'Event'