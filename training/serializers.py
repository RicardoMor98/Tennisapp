from rest_framework import serializers
from .models import TrainingSession
from profiles.serializers import PlayerProfileSerializer

class TrainingSessionSerializer(serializers.ModelSerializer):
    player = PlayerProfileSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=PlayerProfile.objects.all(),
        source='player',
        write_only=True
    )
    duration = serializers.ReadOnlyField()
    
    class Meta:
        model = TrainingSession
        fields = '__all__'

class TrainingSessionDetailSerializer(TrainingSessionSerializer):
    player = PlayerProfileSerializer(read_only=True)