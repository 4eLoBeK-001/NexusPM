from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.workplace, name='workplace'),
    path('teams/', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
]
