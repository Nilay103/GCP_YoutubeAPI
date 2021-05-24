from django_filters import FilterSet


from .models import YouTubeVideo

class YouTubeVideoFilter(FilterSet):
    class Meta:
        model = YouTubeVideo
        fields = {
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'published_date': ['lte', 'gte'],
        }
