from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet

app_name = 'video'

video_router = DefaultRouter()
video_router.register(r'video', VideoViewSet)
