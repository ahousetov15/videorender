import os
import moviepy.editor as mp
from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.files.uploadhandler import InMemoryUploadedFile
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from server.apps.video.models import Video
from .models import Render
from django.db.models import Exists
from .serializers import RenderReadSerializer, RenderWriteSerializer
from pathlib import Path

#if "MEDIA_ROOT" in os.environ:
#from server.settings.components.common import MEDIA_ROOT

#MEDIA_ROOT = os.environ['MEDIA_ROOT']
from server import settings

MEDIA_ROOT = settings.MEDIA_ROOT


class RenderReadView(viewsets.ReadOnlyModelViewSet):
    queryset = Render.objects.all()
    serializer_class = RenderReadSerializer

    def instance_to_memoryfile(self, instance, title):
        inmemotyfilename = title if title else f'render_{instance.title}'
        inmemoryfile = InMemoryUploadedFile(file=instance.video.file,
                                            name=inmemotyfilename,
                                            field_name='render',
                                            content_type='render/mp4',
                                            size=instance.video.size,
                                            charset=None)
        return inmemoryfile

    def make_a_clip(self, instance):
        render_file_name = f'render_{instance.title}.mp4'
        render_file_fullpath = f'{MEDIA_ROOT}/render/{render_file_name}'
        video = mp.VideoFileClip(instance.video.path, target_resolution=(1500, 1500))
        background = (mp.ImageClip(f'{MEDIA_ROOT}/background/background.jpg'))
        text = mp.TextClip('Отрендерено с помощь MoviePy',
                fontsize=95,
                font='DejaVu-Sans-Bold',
                color='blue')
        text = text.set_position('center')
        text.duration = video.duration
        final = mp.CompositeVideoClip([background, video.set_position("center"), text])
        final.duration = video.duration
        final.write_videofile(render_file_fullpath, codec="libx264")
        final.close()
        render_file_size = Path(render_file_fullpath).stat().st_size
        inmemoryfile = InMemoryUploadedFile(file=open(render_file_fullpath, 'rb'),
                                            name=render_file_name,
                                            field_name='render',
                                            content_type='render/mp4',
                                            size=render_file_size,
                                            charset=None)
        return inmemoryfile

    def create_render(self, instance, source):
        inmemoryfile = self.make_a_clip(instance=instance)
        serializer = RenderWriteSerializer(
                                            data={'source':  source,
                                                  'title':   inmemoryfile.name,
                                                  'video':   inmemoryfile
                                                 }
                                           )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return inmemoryfile

    def get_object(self, source):
        try:
            instance = Render.objects.get(source=source)
            inmemoryfile = self.instance_to_memoryfile(instance=instance, title=instance.title)
            return inmemoryfile
        except Render.DoesNotExist:
            raise Http404('No render')


    def retrieve(self, request, *args, **kwargs):
        source = kwargs['pk']
        try:
            inmemoryfile = self.get_object(source=source)
            return FileResponse(inmemoryfile.file,
                                as_attachment=True,
                                filename=inmemoryfile.name)

        except Http404 as h:
            return Response(f"Not found render with 'source' = {source}", status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'],
            detail=False,
            url_path='draw/(?P<pk>\d+)',
            url_name='draw')
    def draw(self, request, pk):
        if Render.objects.filter(source=pk).exists():
            #instance = Render.objects.filter(source=pk)
            return Response(f'Found render with by {pk}!', status.HTTP_302_FOUND)
        else:
            if not Video.objects.filter(pk=pk).exists():
                return Response(f'No video with id == {pk}', status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    instance = Video.objects.get(pk=pk)
                    inmemoryfile = self.create_render(instance=instance, source=pk)
                    return Response(f'Render by key {pk}, was created!', status=status.HTTP_201_CREATED)
                except ValidationError as ve:
                    return Response(f'Invalid data:{ve}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except AssertionError as ae:
                    return Response(f'Assertion error: {ae}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
