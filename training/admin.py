from django import forms
from django.contrib import admin
from datetime import time, datetime
from django.utils import timezone
from django.utils.html import format_html
from .models import TrainingSession, TennisCourt, SessionParticipant


# ---------------- Custom Admin Form ----------------
class TrainingSessionAdminForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        min_hour, max_hour = 8, 21
        now = timezone.localtime()
        today = now.date()

        if self.instance and self.instance.date == today:
            min_hour = max(min_hour, now.hour + 1)

        self.fields['start_time'] = forms.ChoiceField(
            choices=[(time(h, 0), f"{h:02d}:00") for h in range(min_hour, max_hour + 1)]
        )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")

        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
            cleaned_data["start_time"] = start_time

        if start_time:
            end_hour = min(start_time.hour + 1, 22)
            cleaned_data["end_time"] = time(end_hour, 0)

        return cleaned_data


# ---------------- Inline for Participants ----------------
class SessionParticipantInline(admin.TabularInline):
    model = SessionParticipant
    extra = 0
    readonly_fields = ("canceled_at", "status")
    autocomplete_fields = ["player"]


# ---------------- Custom Filter ----------------
class SessionDateFilter(admin.SimpleListFilter):
    title = "Session Date"
    parameter_name = "session_date"

    def lookups(self, request, model_admin):
        return [
            ("upcoming", "Upcoming Sessions"),
            ("past", "Past Sessions"),
            ("all", "All Sessions"),
        ]

    def queryset(self, request, queryset):
        today = timezone.localdate()
        if self.value() == "upcoming" or self.value() is None:
            return queryset.filter(date__gte=today)
        elif self.value() == "past":
            return queryset.filter(date__lt=today)
        elif self.value() == "all":
            return queryset
        return queryset


# ---------------- Admin ----------------
@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    form = TrainingSessionAdminForm
    list_display = [
        "date",
        "court",
        "focus_area",
        "intended_level",  # ADDED: Show intended level in list
        "intensity",
        "colored_status",
        "max_players",
        "start_time",
        "end_time",
        "active_players_count",
        "canceled_players_count",
    ]
    readonly_fields = ["end_time"]
    list_filter = [
        "court", 
        "intended_level",  # ADDED: Filter by intended level
        "intensity", 
        SessionDateFilter, 
        "status"
    ]
    search_fields = ['focus_area', 'court__name']
    date_hierarchy = "date"
    inlines = [SessionParticipantInline]
    actions = ["cancel_selected_sessions"]

    # Colored status display
    def colored_status(self, obj):
        color_map = {
            "canceled": "red",
            "completed": "green",
            "scheduled": "gray",
        }
        color = color_map.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    colored_status.admin_order_field = "status"
    colored_status.short_description = "Status"

    def active_players_count(self, obj):
        return obj.sessionparticipant_set.filter(status='active').count()
    active_players_count.short_description = "Active Players"

    def canceled_players_count(self, obj):
        return obj.sessionparticipant_set.filter(status='canceled').count()
    canceled_players_count.short_description = "Canceled Players"

    @admin.action(description="Cancel selected sessions")
    def cancel_selected_sessions(self, request, queryset):
        updated_count = 0
        for session in queryset:
            if session.status != 'canceled':
                session.status = 'canceled'
                session.save()
                for participant in session.sessionparticipant_set.all():
                    participant.cancel()
                updated_count += 1
        self.message_user(request, f"{updated_count} session(s) canceled.")


# ---------------- Register TennisCourt ----------------
@admin.register(TennisCourt)
class TennisCourtAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "surface_type", "indoor"]
    list_filter = ["surface_type", "indoor"]
    search_fields = ['name', 'location']