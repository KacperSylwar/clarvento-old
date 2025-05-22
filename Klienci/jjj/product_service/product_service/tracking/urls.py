# tracking/urls.py
from django.urls import path
from .views import TrackClickView

urlpatterns = [
    path('api/track-click/', TrackClickView.as_view(), name='track-click'),
]