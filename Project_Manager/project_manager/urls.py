from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler403, handler404, handler500

from decorator_include import decorator_include

from project_manager import views

from projects import views as pviews
from tasks import views as tviews


urlpatterns = [
    path('api/', include('teams.api.urls')),

    path('admin/', admin.site.urls),
    path('', views.main_page, name='home'),

    path('projects/my/', pviews.my_projects, name='my_projects'),
    path('tasks/my/', tviews.my_tasks, name='my_tasks'),


    path('history/', decorator_include(login_required, 'logs.urls', namespace='logs')),
    path('feedback/', views.feedback, name='feedback'),

    path('auth/', include('users.urls', namespace='users')),
    path('workplace/', include('teams.urls', namespace='teams')),
]

handler403 = 'project_manager.views.custom_page_forbidden'
handler404 = 'project_manager.views.custom_page_not_found'
handler500 = 'project_manager.views.custom_server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Django debug toolbar
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]