from django.contrib import admin
from django.utils.html import format_html
from .models import PlayerProfile, CoachProfile, CoachAvailability, CoachReview

# Register your models here.
@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_level', 'age', 'created_at']
    list_filter = ['skill_level', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['age', 'created_at', 'updated_at', 'profile_image_preview']
    fieldsets = (
        (None, {
            'fields': ('user', 'date_of_birth', 'skill_level')
        }),
        ('Media', {
            'fields': ('profile_image', 'profile_image_preview'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.profile_image.url)
        return "No image uploaded"
    profile_image_preview.short_description = 'Profile Image Preview'


@admin.register(CoachProfile)
class CoachProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'certification_level', 'years_experience', 'hourly_rate', 'is_available', 'profile_image_preview']
    list_filter = ['certification_level', 'is_available', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialties']
    readonly_fields = ['created_at', 'updated_at', 'profile_image_preview']
    list_editable = ['is_available']
    fieldsets = (
        ('Media', {
            'fields': ('profile_image', 'profile_image_preview'),
            'classes': ('collapse',)
        }),
        (None, {
            'fields': ('user', 'date_of_birth', 'certification_level')
        }),
        ('Coaching Details', {
            'fields': ('specialties', 'years_experience', 'hourly_rate', 'bio', 'is_available')
        }),
        
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.profile_image.url)
        return "No image uploaded"
    profile_image_preview.short_description = 'Profile Image Preview'


@admin.register(CoachAvailability)
class CoachAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['coach', 'day_of_week', 'start_time', 'end_time']
    list_filter = ['day_of_week', 'coach']
    search_fields = ['coach__user__first_name', 'coach__user__last_name']
    

@admin.register(CoachReview)
class CoachReviewAdmin(admin.ModelAdmin):
    list_display = ['coach', 'player', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['coach__user__first_name', 'coach__user__last_name', 'player__user__first_name', 'player__user__last_name']
    readonly_fields = ['created_at']