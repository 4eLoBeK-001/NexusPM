from django.urls import path

from teams.api import views


urlpatterns = [
    path('teams/', views.get_teams, name='team_list')
]

