from django.db import models

# Create your models here.
class YouTubeVideo(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=100000)
    published_date = models.DateTimeField()
    thumbnail_url = models.URLField(max_length=1000)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]

    @staticmethod
    def get_latest_published_date():
        latest_obj = YouTubeVideo.objects.last()
        return latest_obj.published_date if latest_obj else '1970-01-01T00:00:00Z'
