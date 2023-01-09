import os
import uuid
from datetime import datetime
import requests
from django.core.files import File
from django.http import JsonResponse
from coutoEditor.settings import BASE_URL
from library.path_remover import path_remover
from video.models import TemporaryFiles

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def merger(data):
    file_name = str(uuid.uuid4())
    if not os.path.exists("media/audio-video-merged/"):
        os.mkdir("media/audio-video-merged/")
    a = data['audio']
    v = data['video']
    try:
        r = requests.get(v, stream=True)
        if not r.status_code == 200:
            message = "broken url process could not be completed"
            return JsonResponse({"message": "not successful", "data": message, "status": False})
        if r.status_code == 200:
            filename = str(uuid.uuid4())
            converted_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
            cmd = "ffmpeg -i '{}' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus {}".format(v, converted_video)
            os.system(cmd)
            if not os.path.exists(converted_video):
                message = "video url is broken"
                return JsonResponse({"message": "not successful", "data": message, "status": False})
    except ConnectionError:
        message = "broken url process could not be completed"
        return JsonResponse({"message": "not successful", "data": message, "status": False})
    try:
        r = requests.get(a, stream=True)
        if not r.status_code == 200:
            message = "broken url process could not be completed"
            return JsonResponse({"message": "not successful", "data": message, "status": False})
        if r.status_code == 200:
            pass
    except ConnectionError:
        path_remover(converted_video)
        message = "broken url process could not be completed"
        return JsonResponse({"message": "not successful", "data": message, "status": False})
    filename = str(uuid.uuid4())
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -stream_loop -1 -i {} -i '{}' -vcodec copy -acodec libopus -mapping_family 0 -b:a 96k -shortest -map 0:v:0 -map 1:a:0  {}".format(
        converted_video, a, combined_video)
    os.system(cmd)
    generated_video = open(combined_video, "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=file_name + ".webm"),
                                                   created_at=datetime.utcnow())
    generated_video.close()

    res_dict = {
            "video_url": os.path.join(BASE_URL, video_file.temp_file.url[1:]),
        }
    path_remover(converted_video)
    path_remover(combined_video)
    return JsonResponse({"message": "successful", "data": res_dict, "status": True})