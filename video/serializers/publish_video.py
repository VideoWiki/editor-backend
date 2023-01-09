from video.models import *
from rest_framework import serializers
from video.serializers.user import UserSerializer
from video.serializers.video import VideoSerializer


class PublishVideoSerializer(serializers.ModelSerializer):
    video = VideoSerializer(required=True)
    user = UserSerializer(required=True)
    id = serializers.SerializerMethodField()
    forked_id = serializers.SerializerMethodField()
    published_id = serializers.SerializerMethodField()

    class Meta:
        model = PublishedVideo
        fields = ('id','published_id','forked_id','user','video','is_paid')
        depth = 1

    def get_id(self,obj):
        published_obj = PublishedVideo.objects.get(id=obj.id)
        saved_id = published_obj.saved_video.id
        return saved_id

    def get_forked_id(self,obj):
        try:
            return Fork.objects.get(published_video_id=obj.id).id
        except:
            return None

    def get_published_id(self,obj):
        return obj.id