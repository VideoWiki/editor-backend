from rest_framework import serializers

from backup.videos import TemporaryFiles

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryFiles
        fields = "__all__"

