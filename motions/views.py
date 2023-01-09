from .motion import *
from rest_framework.views import APIView

class ImageVideo(APIView):
	def post(self,request):
		return motion(request.data["image_url"],request.data["motion"])

# class ImagePan(APIView):
# 	def post(self, request):
# 		return imagePan(request.data["image_url"], request.data["type"])