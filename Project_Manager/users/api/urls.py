from django.urls import path

from users.api import views


urlpatterns = [
    path('users/', views.UsersListAPIView.as_view(), name='users_list'),
    path('user/invitations/', views.InvitationListApiView.as_view(), name='invitation_list'),
]

