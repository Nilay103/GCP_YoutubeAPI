from django.db import models
import datetime


class YouTubeVideo(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    published_date = models.DateTimeField()
    thumbnail_url = models.URLField(max_length=1000)

    @staticmethod
    def get_latest_published_date():
        latest_obj = YouTubeVideo.objects.last()
        return latest_obj.published_date if latest_obj else datetime.datetime.fromtimestamp(0)
