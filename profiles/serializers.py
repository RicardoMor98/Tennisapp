from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PlayerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class PlayerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = PlayerProfile
        fields = '__all__'

class PlayerProfileDetailSerializer(PlayerProfileSerializer):
    user = UserSerializer(read_only=True)
    
    def update(self, instance, validated_data):
        # Handle user data if provided
        user_data = self.context['request'].data.get('user', {})
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()
        
        return super().update(instance, validated_data)