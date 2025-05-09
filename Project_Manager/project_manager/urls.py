from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls', namespace='projects')),
    path('auth/', include('users.urls', namespace='users')),
    path('workplace/', include('teams.urls', namespace='teams')),
]
