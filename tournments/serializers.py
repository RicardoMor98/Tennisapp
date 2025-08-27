from rest_framework import serializers
from .models import Tournament, TournamentRegistration
from profiles.serializers import PlayerProfileSerializer
from django.contrib.auth.models import User

class TournamentSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    registrations_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Tournament
        fields = '__all__'

class TournamentRegistrationSerializer(serializers.ModelSerializer):
    player = PlayerProfileSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=PlayerProfile.objects.all(),
        source='player',
        write_only=True
    )
    tournament_name = serializers.ReadOnlyField(source='tournament.name')
    
    class Meta:
        model = TournamentRegistration
        fields = '__all__'

class TournamentDetailSerializer(TournamentSerializer):
    registrations = TournamentRegistrationSerializer(many=True, read_only=True)