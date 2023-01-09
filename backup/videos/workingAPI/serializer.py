from rest_framework.serializers import ModelSerializer
from backup.videos.models import *


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        depth = 1


class SceneSerializer(ModelSerializer):
    class Meta:
        model = Scenes
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
