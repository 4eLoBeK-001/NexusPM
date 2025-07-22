from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_user, name='profile'),
    path('change/profile/', views.change_profile, name='change_profile'),
    path('profile/create/tag/', views.create_user_tag, name='create_user_tag'),
]
