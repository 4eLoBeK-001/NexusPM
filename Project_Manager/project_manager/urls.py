from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from project_manager import views

from projects import views as pviews
from tasks import views as tviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='home'),

    path('projects/my/', pviews.my_projects, name='my_projects'),
    path('tasks/my/', tviews.my_tasks, name='my_tasks'),


    path('history/', include('logs.urls', namespace='logs')),
    path('feedback/', views.feedback, name='feedback'),

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