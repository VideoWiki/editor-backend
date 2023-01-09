from rest_framework.views import APIView
from library.file_dirs import editor_output_dir
from video.editor.recognise_txt import video_to_txt
from video.editor.silence_vid import aud_url
from video.editor.trim import trim_video
from video.editor.speed_vid import speed_up_vid, speed_up_vid_qc
from video.editor.crop_vid import crop_vid
import requests
from django_q.tasks import async_task, result
from django_q.models import Task
from django.http import JsonResponse
import uuid
import os
from video.models import ClipRecords
from rest_framework.response import Response
from coutoEditor.global_variable import BASE_DIR, BASE_URL
from rest_framework import status
import natsort


class caption(APIView):

    def post(self, request):
        video_url = request.data['video_url']
        filename = str(uuid.uuid4())
        chunk_size = 256
        combined_video_url = os.path.join(BASE_DIR, "media/classroom_record/" + filename + ".mp4")
        r = requests.get(video_url, stream=True)
        with open(combined_video_url, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
        whole_text = video_to_txt(combined_video_url)
        return JsonResponse({"message": "Successful", "data": whole_text, "status": True})


class video_chunks(APIView):

    def get(self, request):
        try:
            meeting_id = request.GET.get('meeting_id')
            uid = ClipRecords.objects.filter(meeting_id=meeting_id)[0].uid
            output_dir = BASE_DIR + '/' + editor_output_dir + str(
                uid) + '/'  # editor_output_dir = "media/editor/clip_chunks/"
            dirs = os.listdir(output_dir)
            sorted_dirs = natsort.natsorted(dirs)
            video_url_list = []
            for file in sorted_dirs:
                video_url_list.append(BASE_URL + editor_output_dir + str(uid) + '/' + file)

            return JsonResponse({"message": "Successful",
                                 'data': video_url_list,
                                 "uid": uid,
                                 "meeting_id": meeting_id,
                                 'status': True}
                                )
        except:
            pass

        try:
            uid = request.GET.get('uid')
            meeting_id = ClipRecords.objects.get(uid=uid).meeting_id
            output_dir = BASE_DIR + '/' + editor_output_dir + uid + '/'  # editor_output_dir = "media/editor/clip_chunks/"
            dirs = os.listdir(output_dir)
            sorted_dirs = natsort.natsorted(dirs)
            video_url_list = []
            for file in sorted_dirs:
                video_url_list.append(BASE_URL + editor_output_dir + uid + '/' + file)

            return JsonResponse({"message": "Successful",
                                 'data': video_url_list,
                                 "uid": uid,
                                 "meeting_id": meeting_id,
                                 'status': True}
                                )
        except:
            return Response({"Message": "Invalid meeting id or uid.", "status": False}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):

        if not request.data['task_id']:
            try:
                task_id = async_task('video.editor.clip_chunks.split_to_chunk', request.data["video_url"],
                                 request.data["option"],  request.data["email"])
            except KeyError:
                task_id = async_task('video.editor.clip_chunks.split_to_chunk', request.data["video_url"],
                                     request.data["option"], email=None)
            return JsonResponse({'task_id': task_id})
        else:
            result_dict = result(request.data['task_id'])
            if result_dict is None:
                return JsonResponse({'status': False, 'data': None})
            elif result_dict == "broken url process could not be completed":
                return JsonResponse({
                    'message': "media file is corrupted",
                    'data': result_dict,
                    'status': False,
                    "mail": "not sent",
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({"message": "Successful",
                                     'data': result_dict["data"],
                                     "uid": result_dict["uid"],
                                     "meeting_id": result_dict["meeting_id"],
                                     "mail": result_dict["mail"],
                                     'status': True}
                                    )


class sil_vid(APIView):
    def post(self, request):
        vid_url = request.data['vid_url']
        return aud_url(vid_url)


class trim(APIView):
    def post(self, request):
        video_url = request.data['video_url']
        start = request.data['start']
        end = request.data['end']
        return trim_video(video_url, start, end)

class speed_up_video(APIView):
    def post(self,request):
        video_url = request.data["video_url"]
        speed_factor = request.data["speed_factor"]
        start = request.data["start"]
        end = request.data["end"]
        return speed_up_vid(video_url, speed_factor, start, end)

class crop_video(APIView):
    def post(self,request):
        video_url = request.data["video_url"]
        height = request.data["height"]
        width = request.data["width"]
        x = request.data["x"]
        y = request.data["y"]
        return crop_vid(video_url, height, width, x, y)


class speed_up_vid_qcl(APIView):
    def post(self, request):
        task_id = request.data['task_id']
        if task_id:
            # concatenation process in queue
            task_result = result(task_id)
            if type(task_result) == dict:
                return JsonResponse(task_result)

            elif task_result == None:
                return JsonResponse({
                    'message': "video is in process !",
                    'data': None,
                    'task_id': task_id,
                    'status': True
                })
        task_id = async_task(
            # concatenate videos with translation
            'video.editor.speed_vid.speed_up_vid_qc',
            input_path=request.data["video_url"],
            speed_factor = request.data["speed_factor"],
            start = request.data["start"],
            end = request.data["end"],
        )
        return JsonResponse({
            'message': "speed_vid started ! "
                       "please use task_id to get result ie video ",
            'data': None,
            'task_id': task_id,
            'status': True
        })


