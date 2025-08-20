from django.urls import include, path

from teams.api import views


urlpatterns = [
    path('team/<int:pk>/', include('projects.api.urls', namespace='projects')),

    path('teams/', views.TeamListCreateAPIView.as_view(), name='team_list'),

    path('team/<int:pk>/', include([
        path('', views.TeamDetailAPIView.as_view(), name='team_detail'),

        path('member/<int:member_pk>/role-change/', views.ChangeMemberRoleAPIView.as_view(), name='change_role_member_api'),
        path('members/', views.TeamMembersAPIView.as_view(), name='list_members_api'),
        path('leave/', views.LeaveFromTeamApiView.as_view(), name='leave_from_team_api'),

        path('send/', views.SendInvitationToTeamAPIView.as_view(), name='send_invitation_to_team_api'),

        path('invitations/accept/', views.AcceptInvitationAPIView.as_view(), name='invitation_accept_api'),
    ])),

]

