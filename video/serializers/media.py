from rest_framework.serializers import ModelSerializer
from video.models import *

class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class AudioSerializer(ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'


