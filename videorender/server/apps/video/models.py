from django.db import models
from .validators import video_extension_validator
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='video',
                             max_length=255,
                             blank=False,
                             validators=[video_extension_validator])

    def __str__(self):
        return self.title

