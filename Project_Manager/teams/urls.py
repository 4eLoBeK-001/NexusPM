from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.workplace, name='workplace'),
    path('teams/', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
    path('update/<int:pk>/', views.update_team, name='update_team'),
    path('search/', views.search_team, name='search_team'),
]
