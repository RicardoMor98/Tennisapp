from django.urls import path
from . import views

urlpatterns = [
    path('', views.TrainingSessionList.as_view()),
    path('<int:pk>/', views.TrainingSessionDetail.as_view()),
]