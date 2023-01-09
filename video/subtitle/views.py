from rest_framework.views import APIView
from .video_text_merge import merger
from .video_text_merge_mp4 import merger_mp4
from django_q.tasks import async_task, result
from django_q.models import Task
from django.http import JsonResponse


class videoScript(APIView):

    def post(self, request):

        task_id = request.data['task_id']
        if task_id:
            # concatenation process in queue
            task_result = result(task_id)
            if type(task_result) == dict:
                return JsonResponse(task_result)

            elif task_result == None:
                return JsonResponse({
                    'message': "video-text merge is in process !",
                    'data': None,
                    'task_id': task_id,
                    'status': True
                })
        task_id = async_task(
            # concatenate videos with translation
            'video.subtitle.video_text_merge.merger',
            script=request.data["script"],
            url = request.data["url"],
            bg_opacity = request.data["bg_opacity"],
            transition_type = request.data["transition_type"],
            font_color = request.data["font_color"],
            background_color = request.data["background_color"],
            text_position = request.data["text_position"]
        )
        return JsonResponse({
            'message': "video-text merge started ! "
                       "please use task_id to get result ie video ",
            'data': None,
            'task_id': task_id,
            'status': True
        })


class videoScript_mp4(APIView):

    def post(self, request):

        task_id = request.data['task_id']
        if task_id:
            # concatenation process in queue
            task_result = result(task_id)
            if type(task_result) == dict:
                return JsonResponse(task_result)

            elif task_result == None:
                return JsonResponse({
                    'message': "video-text merge is in process !",
                    'data': None,
                    'task_id': task_id,
                    'status': True
                })
        task_id = async_task(
            # concatenate videos with translation
            'video.subtitle.video_text_merge_mp4.merger_mp4',
            script=request.data["script"],
            url = request.data["url"],
            bg_opacity = request.data["bg_opacity"],
            transition_type = request.data["transition_type"],
            font_color = request.data["font_color"],
            background_color = request.data["background_color"],
            text_position = request.data["text_position"]
        )
        return JsonResponse({
            'message': "video-text merge started ! "
                       "please use task_id to get result ie video ",
            'data': None,
            'task_id': task_id,
            'status': True
        })

# old backup code
# class videoScript(APIView):
#     def post(self, request):
#         return merger(request)
# class videoScript_mp4(APIView):
#     def post(self, request):
#         return merger_mp4(request)