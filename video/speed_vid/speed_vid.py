import os
import urllib.request
import uuid
from coutoEditor.global_variable import BASE_URL, BASE_DIR
from library.file_dirs import editor_speedUp_output_dir, editor_speedUp_temp_dir
from video.models import TemporaryFiles
from django.core.files import File
from datetime import datetime
import urllib
from video.models import ClipRecords
from rest_framework.response import Response
import requests
from rest_framework import status


def convert_to_sec(s):
    l = list(map(int, s.split(':')))
    return sum(n * sec for n, sec in zip(l[::-1], (1, 60, 3600)))


def speed_up_vid(input_path, speed_factor, start, end):

    '''
    Method Params:
    input_path: The video file url or directory path file name
    speed_factor: The factor for the speed up process
    start: start of the video part that needs to be sped up (in secs)
    end: end of the video part that needs to be sped up (in secs)
    '''

    start = convert_to_sec(start)
    end = convert_to_sec(end)

    filename = str(uuid.uuid4())
    temporary_dir = BASE_DIR + '/' + editor_speedUp_temp_dir  # editor_temp_dir = media/editor/speed_vid/temp/"
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

    if not os.path.exists(temporary_dir):
        os.mkdir(temporary_dir)

    stream = os.popen(
        "ffmpeg.ffprobe -loglevel error -select_streams a -show_entries stream=codec_type -of csv=p=0 '{}'".format(
            input_path))
    output = stream.read()
    if len(output) == 0:
        input_path_vid = os.path.join(BASE_DIR, temporary_dir) + filename + "_temp_video.mp4"
        cmd = "ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i '{}' -c:v copy -c:a aac -shortest {}".format(
            input_path, input_path_vid)
        os.system(cmd)
    else:
        # check if it's a directory or a url
        if(os.path.isfile(input_path)):
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

    output_path = os.path.join(BASE_DIR, editor_speedUp_output_dir + filename + ".mp4")

    cmd = 'ffmpeg -i ' + input_path_vid + ' \
            -filter_complex \
            "[0:v]trim=0:' + str(start) + ',setpts=PTS-STARTPTS[v1]; \
            [0:v]trim=' + str(start) + ':' + str(end) + ',setpts=1/' + str(speed_factor) + '*(PTS-STARTPTS)[v2]; \
            [0:v]trim=' + str(end) + ',setpts=PTS-STARTPTS[v3]; \
            [0:a]atrim=0:' + str(start) + ',asetpts=PTS-STARTPTS[a1]; \
            [0:a]atrim=' + str(start) + ':' + str(end) + ',asetpts=PTS-STARTPTS,atempo=' + str(speed_factor) + '[a2]; \
            [0:a]atrim=' + str(end) + ',asetpts=PTS-STARTPTS[a3]; \
            [v1][a1][v2][a2][v3][a3]concat=n=3:v=1:a=1" \
            -preset superfast -profile:v baseline ' + output_path

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
    return res_dict










