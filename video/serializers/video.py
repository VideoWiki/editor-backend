from rest_framework.serializers import ModelSerializer

from coutoEditor.global_variable import BASE_URL
from video.models import Video
from rest_framework import serializers


class VideoSerializer(ModelSerializer):
    url = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_url(self, obj):
        url = f'{BASE_URL[:-1]}{obj.video_file.url}'
        return url

    def get_thumbnail(self, obj):
        url = f'{BASE_URL[:-1]}{obj.thumbnail.url}'
        return url

    class Meta:
        model = Video
        exclude = ('video_file', )
        depth = 1
