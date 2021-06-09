from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_video = serializer.save()
        headers = self.get_success_headers(serializer.data)
        new_video_id = new_video.pk
        return Response(new_video_id, status=status.HTTP_201_CREATED, headers=headers)
