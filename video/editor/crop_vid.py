import os
import uuid
from coutoEditor.global_variable import BASE_URL, BASE_DIR
from library.file_dirs import editor_speedUp_output_dir, editor_speedUp_temp_dir
from video.models import TemporaryFiles
from django.core.files import File
from datetime import datetime
from rest_framework.response import Response
import requests
from rest_framework import status
from library.path_remover import path_remover

def crop_vid(input_path, height, width, x, y):

    '''
    Method Params:
    input_path: The video file url or directory path file name
    height: height of the cropped window
    width: width of the cropped window
    x: top left x axis value of the cropped window
    y: top left y axis value of the cropped window
    '''

    filename = str(uuid.uuid4())
    output_dir = BASE_DIR + '/' + editor_speedUp_output_dir  # editor_speedUp_output_dir = media/editor/speed_vid/

    # Check for broken url
    r = requests.get(input_path, stream=True)
    if not r.status_code == 200:
        return Response({
            'message': "media file is corrupted",
            'data': "broken url process could not be completed",
            'status': False
        }, status=status.HTTP_400_BAD_REQUEST)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_path = os.path.join(BASE_DIR, editor_speedUp_output_dir + filename + ".mp4")

    cmd = "ffmpeg -i '{}' -filter:v 'crop={}:{}:{}:{}' -c:a copy ".format(input_path, str(width), str(height), str(x),
                                                                          str(y)) + output_path

    os.system(cmd)

    generated_video = open(output_path, "rb")
    generated_video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                                         created_at=datetime.utcnow())
    generated_video.close()

    path_remover(output_path)

    res_dict = {}
    res_dict["video_url"] = os.path.join(BASE_URL, generated_video_file.temp_file.url[1:])
    return Response({"message": "Successful", "data": res_dict, "status": True})










