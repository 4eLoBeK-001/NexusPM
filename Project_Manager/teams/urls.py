from django.urls import include, path

from . import views

app_name = 'teams'

urlpatterns = [
    path('team/<int:pk>/', include('projects.urls', namespace='projects')),

    path('', views.workplace, name='workplace'),

    path('team/<int:pk>/', include([
        path('conf/', views.team_conf, name='team_conf'),
        path('members/', views.team_members, name='team_members'),
        path('members/adds/', views.send_invitation_to_team, name='send_invitation_to_team'),
        path('member/<int:member_pk>/delete/', views.deleting_team_members, name='deleting_team_members'),
        path('members/search/', views.search_team_members, name='search_team_members'),
        path('member/<int:member_pk>/role-change/', views.change_role_member, name='change_role_member'),

        path('roles/', views.access_rights, name='roles'),
        
        path('change/', views.change_team, name='change_team'),
        path('delete/', views.delete_team, name='delete_team'),
        path('leave/', views.leave_from_team, name='leave_from_team'),
    ])),
    
    
    path('teams/', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
    path('search/', views.search_team, name='search_team'),
    path('ssearch/', views.sidebar_search_team, name='sidebar_search_team'),
]
