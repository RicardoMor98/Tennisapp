from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import PlayerProfile
from .serializers import PlayerProfileSerializer, PlayerProfileDetailSerializer
from tennisapp.permissions import IsOwnerOrReadOnly

# Create your views here.
class PlayerProfileList(generics.ListAPIView):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer

class PlayerProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileDetailSerializer
    
    def get_object(self):
        # Allow users to access their own profile by ID or by 'me'
        if self.kwargs['pk'] == 'me':
            return self.request.user.playerprofile
        return super().get_object()