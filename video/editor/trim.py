import os
import uuid
from django.http import JsonResponse
from coutoEditor.global_variable import BASE_URL, BASE_DIR
from library.file_dirs import editor_temp_dir
from video.models import TemporaryFiles
from django.core.files import File
from datetime import datetime
import urllib.request
from rest_framework.response import Response
import requests
from rest_framework import status

def trim_video(input_path, start, end):
    '''
    start: The start time of the trimmed video
    end: The end time of the trimmed video
    input_path: The file path (or url) of the source video
    output_path: The file path of the trimmed video

    '''
    filename = str(uuid.uuid4())

    temporary_dir = BASE_DIR + '/' + editor_temp_dir  # editor_temp_dir = media/editor/clip_chunks/temp/"

    # Check for broken url
    r = requests.get(input_path, stream=True)
    if not r.status_code == 200:
        return Response({
            'message': "media file is corrupted",
            'data': "broken url process could not be completed",
            'status': False
        }, status=status.HTTP_400_BAD_REQUEST)

    if not os.path.exists(temporary_dir):
        os.mkdir(temporary_dir)

    if (os.path.isfile(input_path)):  # todo handle this case
        input_path_vid = BASE_DIR + input_path
        pass
    else:
        ext_name = filename + '_temp_video.mp4'
        ext_path = temporary_dir + ext_name
        r = requests.get(input_path)
        with open(ext_path, 'wb') as outfile:
            outfile.write(r.content)
        outfile.close()
        input_path_vid = ext_path

    output_path = os.path.join(BASE_DIR, "media/editor/trim" + filename + ".mp4")
    cmd = "ffmpeg -i " + input_path_vid + " -ss  " + start + " -to " + end + " -c:v libx264 -c:a copy " + output_path
    os.system(cmd)

    generated_video = open(output_path, "rb")
    generated_video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                                         created_at=datetime.utcnow())
    generated_video.close()

    if os.path.exists(input_path_vid):
        os.remove(input_path_vid)

    if os.path.exists(output_path):
        os.remove(output_path)

    res_dict = {}
    res_dict["video_url"] = os.path.join(BASE_URL, generated_video_file.temp_file.url[1:])
    return JsonResponse({"message": "Successful", "data": res_dict, "status": True})
