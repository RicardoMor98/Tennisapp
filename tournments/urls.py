from django.urls import path
from . import views

urlpatterns = [
    path('', views.TournamentList.as_view()),
    path('<int:pk>/', views.TournamentDetail.as_view()),
    path('<int:tournament_id>/registrations/', views.TournamentRegistrationList.as_view()),
    path('<int:tournament_id>/registrations/<int:pk>/', views.TournamentRegistrationDetail.as_view()),
]