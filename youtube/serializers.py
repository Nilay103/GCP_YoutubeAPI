from rest_framework import serializers

from .models import YouTubeVideo

class YouTubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = '__all__'
