from django.http import JsonResponse
from rest_framework.views import APIView
from .sentence_keyword_detect.scene_creation import scene_creation

class SentenceDetection(APIView):

    def post(self, request):
        if request.method == 'POST':

            text = request.data['text']
            break_type = request.data['break_type']
            scenes = scene_creation(text, break_type)

            return JsonResponse(scenes)
