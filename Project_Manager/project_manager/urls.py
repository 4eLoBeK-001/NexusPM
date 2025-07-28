from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from project_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='home'),

    path('auth/', include('users.urls', namespace='users')),
    path('workplace/', include('teams.urls', namespace='teams')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Django debug toolbar
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]