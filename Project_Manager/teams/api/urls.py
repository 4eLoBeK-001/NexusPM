from django.urls import include, path

from teams.api import views


urlpatterns = [
    path('', include('projects.api.urls', namespace='projects')),

    path('teams/', views.TeamListCreateAPIView.as_view(), name='team_list'),
    path('team/<int:pk>/', views.TeamDetailAPIView.as_view(), name='team_detail'),

    path('team/<int:pk>/member/<int:member_pk>/role-change/', views.ChangeMemberRoleAPIView.as_view(), name='change_role_member_api'),
    path('team/<int:pk>/members/', views.TeamMembersAPIView.as_view(), name='list_members_api'),
    path('team/<int:pk>/leave/', views.LeaveFromTeamApiView.as_view(), name='leave_from_team_api'),

    path('team/<int:pk>/send/', views.SendInvitationToTeamAPIView.as_view(), name='send_invitation_to_team_api'),

    path('team/<int:pk>/invitations/accept/', views.AcceptInvitationAPIView.as_view(), name='invitation_accept_api'),
    

    path('a/', views.TeamsDetailAPIView.as_view(), name='a'), # ПОТОМ УДАЛИТЬ
]

