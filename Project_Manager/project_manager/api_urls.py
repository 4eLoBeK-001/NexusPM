from django.urls import path, include
from teams.api import views


urlpatterns = [
    path('roles/', views.TeamRolesAPIView.as_view(), name='roles'),

    path('', include('teams.api.urls')),
    path('', include('users.api.urls')),
]