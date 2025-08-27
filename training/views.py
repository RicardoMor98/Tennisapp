from django.shortcuts import render
from rest_framework import generics, permissions
from .models import TrainingSession
from .serializers import TrainingSessionSerializer, TrainingSessionDetailSerializer
from tennisapp.permissions import IsOwnerOrReadOnly

# Create your views here.
class TrainingSessionList(generics.ListCreateAPIView):
    serializer_class = TrainingSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # If user is staff, show all sessions
        if self.request.user.is_staff:
            return TrainingSession.objects.all()
        # Otherwise, only show sessions for the current user
        return TrainingSession.objects.filter(player__user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the player to the current user's profile
        profile = self.request.user.playerprofile
        serializer.save(player=profile)

class TrainingSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionDetailSerializer