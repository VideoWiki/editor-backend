from rest_framework.serializers import ModelSerializer

from video.models import *
from video.serializers.user import UserSerializer
from video.serializers.video import VideoSerializer


class SaveVideoSerializer(ModelSerializer):
    video = VideoSerializer(required=True)
    user = UserSerializer(required=True)


    class Meta:
        model = SavedVideo
        fields = '__all__'
        depth = 1


class SceneSerializer(ModelSerializer):
    class Meta:
        model = Scenes
        fields = '__all__'


class SubtitleSerializer(ModelSerializer):
    class Meta:
        model = Subtitle
        fields = '__all__'
