from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from planner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('planner.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth2callback/', views.google_calendar_redirect_view, name='calendar_redirect'),
    path('calendar/init/', views.google_calendar_init_view, name='google_calendar_init'),
    path('calendar/init/<int:event_id>/', views.google_calendar_init_view, name='google_calendar_init_event'),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
