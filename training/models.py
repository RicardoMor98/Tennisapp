from django.db import models
from profiles.models import PlayerProfile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, time

# ---------------- Tennis Court ----------------
class TennisCourt(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    surface_type = models.CharField(
        max_length=50,
        choices=[("Clay", "Clay"), ("Grass", "Grass"), ("Hard", "Hard"), ("Carpet", "Carpet")],
        default="Hard"
    )
    indoor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.surface_type})"


# ---------------- Training Session ----------------
class TrainingSession(models.Model):
    # Use the same skill levels as PlayerProfile
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('competition', 'Competition'),
    ]
    
    court = models.ForeignKey(
        TennisCourt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sessions"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    focus_area = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    intensity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rate intensity from 1 (low) to 10 (high)"
    )
    max_players = models.IntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(4)],  # Ensure max is 4
        help_text="Maximum 4 players allowed per session"
    )
    intended_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVELS,
        default='intermediate',
        help_text="Intended skill level for this session"
    )

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    players = models.ManyToManyField(
        PlayerProfile,
        through='SessionParticipant',
        related_name='training_sessions'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']

    # ---------------- Validation ----------------
    def clean(self):
        now = timezone.localtime()

        # Always auto-set end_time if missing
        if self.start_time and not self.end_time:
            dt_start = datetime.combine(self.date, self.start_time)
            dt_end = dt_start + timedelta(hours=1)
            if dt_end.time() > time(22, 0):
                dt_end = datetime.combine(self.date, time(22, 0))
            self.end_time = dt_end.time()

        # Validate max_players doesn't exceed 4
        if self.max_players > 4:
            raise ValidationError({"max_players": "Maximum 4 players allowed per session."})

        # Only validate if both start & end exist
        if self.start_time and self.end_time:
            session_start = timezone.make_aware(datetime.combine(self.date, self.start_time))
            session_end = timezone.make_aware(datetime.combine(self.date, self.end_time))

            # 1. Cannot book past sessions (when creating new)
            if session_start < now and not self.pk:
                raise ValidationError("Cannot book a session in the past.")

            # 2. Allowed hours
            if not (time(8, 0) <= self.start_time <= time(21, 0)):
                raise ValidationError({"start_time": "Start time must be between 08:00 and 21:00."})
            if not (time(9, 0) <= self.end_time <= time(22, 0)):
                raise ValidationError({"end_time": "End time must be between 09:00 and 22:00."})

            # 3. Duration must be 1h
            duration_hours = (session_end - session_start).total_seconds() / 3600
            if duration_hours != 1:
                raise ValidationError("Training session must be exactly 1 hour long.")

            # 4. No overlapping sessions on the same court
            overlapping = TrainingSession.objects.filter(
                court=self.court,
                date=self.date,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)
            if overlapping.exists():
                raise ValidationError("This court is already booked during this time.")

    # ---------------- Save override ----------------
    def save(self, *args, **kwargs):
        # Ensure max_players doesn't exceed 4
        if self.max_players > 4:
            self.max_players = 4
            
        # Auto-set end_time before saving
        if self.start_time:
            dt_start = datetime.combine(self.date, self.start_time)
            dt_end = dt_start + timedelta(hours=1)
            if dt_end.time() > time(22, 0):
                dt_end = datetime.combine(self.date, time(22, 0))
            self.end_time = dt_end.time()

        # Auto-complete sessions if already in the past
        now = timezone.localtime()
        
        # FIX: Create timezone-aware datetime for comparison
        session_start_naive = datetime.combine(self.date, self.start_time)
        session_start = timezone.make_aware(session_start_naive)
        session_end = session_start + timedelta(hours=1)

        if self.status == 'scheduled' and session_end < now:
            self.status = 'completed'

        self.full_clean()
        super().save(*args, **kwargs)

    # ---------------- Helpers ----------------
    def duration(self):
        return (datetime.combine(self.date, self.end_time) - datetime.combine(self.date, self.start_time)).total_seconds() / 3600

    def __str__(self):
        return f"Session on {self.date} ({self.focus_area}) - {self.intended_level}"

    def check_auto_cancel(self):
        canceled_count = self.sessionparticipant_set.filter(status='canceled').count()
        if canceled_count >= 3 and self.status != 'canceled':
            self.status = 'canceled'
            self.save()

    def add_player(self, player):
        if self.players.count() >= self.max_players:
            raise ValueError("Session is full")
        SessionParticipant.objects.create(session=self, player=player)

    def remove_player(self, player, by_admin=False):
        """Users can cancel only 24h before. Admin can cancel anytime."""
        try:
            participant = SessionParticipant.objects.get(session=self, player=player)
            now = timezone.localtime()
            
            # FIX: Create timezone-aware datetime for comparison
            session_start_naive = datetime.combine(self.date, self.start_time)
            session_start = timezone.make_aware(session_start_naive)
            
            if by_admin or (session_start - now >= timedelta(hours=24)):
                participant.cancel()
            else:
                raise ValidationError("You can only cancel this session 24 hours before it starts.")
        except SessionParticipant.DoesNotExist:
            pass

    def get_participant_status(self):
        active = self.sessionparticipant_set.filter(status='active').select_related('player')
        canceled = self.sessionparticipant_set.filter(status='canceled').select_related('player')
        return {
            'active': [p.player for p in active],
            'canceled': [p.player for p in canceled]
        }

    def participant_summary(self):
        status = self.get_participant_status()
        return {
            'active_count': len(status['active']),
            'canceled_count': len(status['canceled']),
            'is_full': len(status['active']) >= self.max_players,
            'is_canceled': self.status == 'canceled'
        }


# ---------------- Session Participant ----------------
class SessionParticipant(models.Model):
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)

    PARTICIPANT_STATUS = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=10, choices=PARTICIPANT_STATUS, default='active')
    canceled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('session', 'player')

    def cancel(self):
        self.status = 'canceled'
        self.canceled_at = timezone.now()
        self.save()
        self.session.check_auto_cancel()

    def __str__(self):
        return f"{self.player.user.get_full_name()} - {self.session}"