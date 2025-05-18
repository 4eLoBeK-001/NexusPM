from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls', namespace='projects')),
    path('auth/', include('users.urls', namespace='users')),
    path('workplace/', include('teams.urls', namespace='teams')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)