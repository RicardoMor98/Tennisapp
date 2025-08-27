from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlayerProfileList.as_view()),
    path('<int:pk>/', views.PlayerProfileDetail.as_view()),
    path('me/', views.PlayerProfileDetail.as_view(), {'pk': 'me'}),
]