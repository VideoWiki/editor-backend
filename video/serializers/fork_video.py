from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .user import UserSerializer
from video.serializers.video import VideoSerializer
from video.models import *

class SaveVideoSerializer(ModelSerializer):
    class Meta:
        model = SavedVideo
        fields = ('id',)
        depth = 1

class ForkVideoSerializer(ModelSerializer):
    user = UserSerializer(required=True)
    video = serializers.SerializerMethodField()
    # save video id
    id = serializers.SerializerMethodField()
    forked_id = serializers.SerializerMethodField()
    is_paid = serializers.SerializerMethodField()


    class Meta:
        model = Fork
        fields = ('id','published_video','forked_id','user','video', 'is_paid',)

    def get_video(self, obj):
        return VideoSerializer(Video.objects.get(
            publishedvideo__fork=obj.id),
            required=False,
            default=None
        ).data

    def get_id(self,obj):
        published_obj = PublishedVideo.objects.get(id=obj.published_video.id)
        saved_id = published_obj.saved_video.id
        return saved_id

    def get_forked_id(self,obj):
        return obj.id

    def get_is_paid(self,obj):
        published_obj = PublishedVideo.objects.get(id=obj.published_video.id)
        is_paid = published_obj.is_paid
        return is_paid
