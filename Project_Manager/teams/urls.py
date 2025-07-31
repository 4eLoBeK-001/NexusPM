from django.urls import include, path

from . import views

app_name = 'teams'

urlpatterns = [
    path('team/', include('projects.urls', namespace='projects')),

    path('', views.workplace, name='workplace'),
    path('team/<int:pk>/conf/', views.team_conf, name='team_conf'),
    path('team/<int:pk>/members/', views.team_members, name='team_members'),
    path('team/<int:pk>/members/adds/', views.send_invitation_to_team, name='send_invitation_to_team'),
    path('team/<int:pk>/member/<int:member_pk>/delete/', views.deleting_team_members, name='deleting_team_members'),
    path('team/<int:pk>/members/search/', views.search_team_members, name='search_team_members'),
    
    path('teams/', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
    path('change/<int:pk>/', views.change_team, name='change_team'),
    path('delete/<int:pk>/', views.delete_team, name='delete_team'),
    path('search/', views.search_team, name='search_team'),
    path('ssearch/', views.sidebar_search_team, name='sidebar_search_team'),
]
