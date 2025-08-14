from django.urls import path

from teams.api import views


urlpatterns = [
    path('teams/', views.TeamListCreateAPIView.as_view(), name='team_list'),
    path('team/<int:pk>/', views.TeamDetailAPIView.as_view(), name='team_detail'),
    
    
    
    path('a/', views.TeamsDetailAPIView.as_view(), name='a'), # ПОТОМ УДАЛИТЬ
]

