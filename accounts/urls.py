from django.urls import path
from .views import upload_background

urlpatterns = [
    path('upload-background/', upload_background, name='upload_background'),
]
