from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/<int:user_id>/', include([
        path('', views.profile_user, name='profile'),
        path('change/', views.change_profile, name='change_profile'),
        path('privace-settings/', views.private_profile, name='private_profile'),
        path('privace-change/', views.change_privacy_profile, name='change_privacy_profile'),
        path('create/tag/', views.create_user_tag, name='create_user_tag'),
        path('create/social/', views.add_social_network, name='add_social_network'),
    ])),

    path('delete/tag/<int:tag_pk>/', views.delete_user_tag, name='delete_user_tag'),

    path('profile/delete/social/<int:network_pk>/', views.delete_social_network, name='delete_social_network'),
    
    path('invitations/', views.team_invitations, name='invitations'),
    path('invitations/search/', views.search_invitations, name='search_notifications'),
   
    path('invitation/<int:invitation_id>/accept/', views.accept_invitation, name='accept_invitation'),
]
