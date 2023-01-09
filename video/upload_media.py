from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from .models import TemporaryFiles
from coutoEditor.settings import BASE_URL
from django_q.tasks import async_task, result
from django.http import JsonResponse

# class FileUploadView(APIView):
#     def post(self, request, *args, **kwargs):
#
#       file = TemporaryFiles.objects.create(
#           temp_file=request.data['media'],
#           created_at=datetime.utcnow()
#       )
#       return Response({"media_url":BASE_URL+file.temp_file.url[1:]},status=status.HTTP_201_CREATED)

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        if request.data['task_id'] == "null":
            try:
                task_id = async_task('video.upload_media.file_uploader', request.data["media"])
            except KeyError:
                task_id = async_task('video.upload_media.file_uploader', request.data["media"])
            return JsonResponse({'task_id': task_id})
        else:
            result_dict = result(request.data['task_id'])
            if result_dict is None:
                return JsonResponse({'status': False, 'data': None})
            else:
                return JsonResponse({'status': True, 'data': result_dict})

def file_uploader(media):
    file = TemporaryFiles.objects.create(temp_file=media,created_at=datetime.utcnow())
    return {"media_url":BASE_URL+file.temp_file.url[1:]}