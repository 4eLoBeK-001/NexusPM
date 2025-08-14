from django.urls import path

from teams.api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('teams/', views.TeamListCreateAPIView.as_view(), name='team_list'),
    path('team/<int:pk>/', views.TeamDetailAPIView.as_view(), name='team_detail'),

    path('team/<int:pk>/member/<int:member_pk>/role-change/', views.ChangeMemberRoleAPIView.as_view(), name='change_role_member_api'),

    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('a/', views.TeamsDetailAPIView.as_view(), name='a'), # ПОТОМ УДАЛИТЬ
]

