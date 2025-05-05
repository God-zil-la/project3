from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('new/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/edit/', views.event_update, name='event_update'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Google Calendar OAuth for all events
    path('calendar/init/', views.google_calendar_init_view, name='calendar_init'),
    path('oauth2callback/', views.google_calendar_redirect_view, name='calendar_redirect'),

    # Sync a specific event
    path('<int:event_id>/sync/', views.sync_to_google, name='sync_to_google'),
]
