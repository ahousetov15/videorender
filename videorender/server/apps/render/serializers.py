from rest_framework import serializers
from .models import Render
from server.apps.video.models import Video
from server.apps.video.serializers import VideoSerializer


class RenderSerializer(serializers.ModelSerializer):
    source = VideoSerializer()
    title = serializers.CharField(max_length=310)
    video = serializers.FileField(max_length=310)

    class Meta:
        model = Render
        fields = ('source', 'title', 'video')


class RenderWriteSerializer(RenderSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    class Meta:
        model = Render
        fields = ('source', 'title', 'video')


class RenderReadSerializer(RenderSerializer):
    class Meta:
        model = Render
        fields = ('source', 'title', 'video')
