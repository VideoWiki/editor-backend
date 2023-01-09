from django_q.tasks import async_task, result
from django_q.models import Task
from rest_framework.views import APIView
from .concat import single_video_concat
from django.http import JsonResponse
from rest_framework import status
import datetime
from coutoEditor.global_variable import BASE_DIR


class VideoPreviewMaker(APIView):

    def post(self, request):

        task_id = request.data['task_id']
        if task_id:
            # concatenation process in queue
            task_result = result(task_id)
            if task_result == "broken url process could not be completed":
                dir = BASE_DIR + "/logs/concat_logs/concat.txt"
                with open(dir, "a") as f:
                    f.write("\n" + str(datetime.datetime.now()) + " ERROR " + "{} ".format(str(task_result[
                                                                                                   0])) + "{" + " 'videos': {}, 'width': {}, 'height': {}, 'bgm_url': {}, 'motions': {}".format(
                        str(task_result[1]), str(task_result[2]), str(task_result[3]), str(task_result[4]),
                        str(task_result[5]) + "}"))
                f.close()
                return JsonResponse({
                    'message': "media file is corrupted",
                    'data': task_result,
                    'task_id': task_id,
                    'status': False
                }, status=status.HTTP_400_BAD_REQUEST)

            elif task_result == None:
                return JsonResponse({
                    'message': "concatenation is in process !",
                    'data': None,
                    'task_id': task_id,
                    'status': True
                })

            elif len(task_result)==2:
                return JsonResponse({
                    'message': "Successful",
                    'data': task_result,
                    'task_id': task_id,
                    'status': True
                })
            elif len(task_result)==3:
                return JsonResponse({
                    'message': "Successful",
                    'data': task_result,
                    'task_id': task_id,
                    'status': True
                })
            else:
                dir = BASE_DIR + "/logs/concat_logs/concat.txt"
                with open(dir, "a") as f:
                    f.write("\n" + str(datetime.datetime.now()) + " ERROR "+ "{} ".format(str(task_result[0])) + "{" + " 'videos': {}, 'width': {}, 'height': {}, 'bgm_url': {}, 'motions': {}".format(str(task_result[1]), str(task_result[2]), str(task_result[3]), str(task_result[4]), str(task_result[5]) +"}") )
                f.close()
                return JsonResponse({
                    'message': "un_successful",
                    'data': task_result[0],
                    'task_id': task_id,
                    'status': False
                }, status=status.HTTP_400_BAD_REQUEST)

        # concatenation process started
        videos = request.data['videos']
        if len(videos) == 1:
            task_id = async_task(
                # concatenate videos with translation
                'video.concat.concat.single_video_concat',
                request.data["videos"],
                request.data['bgm'],
                request.data['width'],
                request.data['height'],
                email=request.data['email'],
            )
            return JsonResponse({
                'message': "concatenation started ! "
                           "please use task_id to get result ie video ",
                'data': None,
                'task_id': task_id,
                'status': True
            })

        try:
            motions = request.data['motions']
        except KeyError:
            motions = []

        task_id = async_task(
            # concatenate videos with translation
            'video.concat.concat.translated_concatenation',
            videos,
            motions,
            request.data['width'],
            request.data['height'],
            bgm_url=request.data['bgm'],
            email=request.data['email'],
        )
        return JsonResponse({
            'message': "concatenation started ! "
                       "please use task_id to get result ie video ",
            'data': None,
            'task_id': task_id,
            'status': True
        })


class TaskRemoveView(APIView):
    def post(self, request):
        return JsonResponse({'message': "Not Successful", 'data': "task has been deleted", 'status': False})
