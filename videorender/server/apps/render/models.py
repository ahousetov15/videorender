from django.db import models
from server.apps.video.models import Video


class Render(models.Model):
    source = models.ForeignKey(Video,
                               on_delete=models.PROTECT,
                               verbose_name='Источник видео',
                               related_name='source')
    title = models.CharField(max_length=310)
    video = models.FileField(upload_to='render', max_length=310)

    def __str__(self):
        return self.title
