
from rest_framework.serializers import ModelSerializer
from video.models import Tags

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
