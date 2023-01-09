from rest_framework.views import APIView
from .merge import merger
from .merger_mp4 import merger_mp4

class AudioVideoMerge(APIView):
	def post(self,request):
		data={
			"audio":request.data["audio"],
			"video":request.data["video"],
		}
		return merger(data)


class AudioVideoMerge_mp4(APIView):
	def post(self,request):
		data={
			"audio":request.data["audio"],
			"video":request.data["video"],
		}
		return merger_mp4(data)

