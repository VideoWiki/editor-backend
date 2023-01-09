from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MusicLib
from  .serializer import MusicSerializer
from rest_framework import status


class MusicList(APIView):
    def get(self, request):

        if request.GET.get("genre")=="all":
            music = MusicLib.objects.all().exclude(file="").order_by("title")
        else:
            music = MusicLib.objects.filter(
                genre=request.GET.get("genre")).exclude(file="").order_by("title")
        musicserializer = MusicSerializer(music, many=True)

        return  Response({"message": "successful", 'data': musicserializer.data, "status": True})




