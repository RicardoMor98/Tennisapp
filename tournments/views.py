from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Tournament, TournamentRegistration
from .serializers import TournamentSerializer, TournamentDetailSerializer, TournamentRegistrationSerializer
from tennisapp.permissions import IsOwnerOrReadOnly

# Create your views here.
class TournamentList(generics.ListCreateAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Tournament.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Tournament.objects.all()
    serializer_class = TournamentDetailSerializer

class TournamentRegistrationList(generics.ListCreateAPIView):
    serializer_class = TournamentRegistrationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return TournamentRegistration.objects.filter(tournament_id=tournament_id)
    
    def perform_create(self, serializer):
        tournament_id = self.kwargs['tournament_id']
        tournament = Tournament.objects.get(id=tournament_id)
        
        # Check if user already registered
        user_profile = self.request.user.playerprofile
        if TournamentRegistration.objects.filter(tournament=tournament, player=user_profile).exists():
            raise serializers.ValidationError("You are already registered for this tournament")
        
        serializer.save(tournament=tournament, player=user_profile)

class TournamentRegistrationDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TournamentRegistrationSerializer
    
    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return TournamentRegistration.objects.filter(tournament_id=tournament_id)