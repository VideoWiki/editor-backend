from rest_framework.response import Response
from moviepy.editor import *
from coutoEditor.settings import BASE_DIR
from uuid import uuid4
import requests
from coutoEditor.settings import BASE_URL
from django.core.files import File
from video.models import TemporaryFiles
from datetime import datetime
from library.path_remover import path_remover

def imagePan(image_url,motion):
    filename=str(uuid4())
    res_dict = {}
    combined_url = os.path.join(BASE_DIR, "media/images/" + filename +"."+image_url.split(".")[-1])
    vid_out = os.path.join(BASE_DIR, "media/images/" + filename + ".mp4")
    if not os.path.exists(os.path.join(BASE_DIR,"media/images/")):
        os.mkdir(os.path.join(BASE_DIR,"media/images/"))
    r=requests.get(image_url)
    open(combined_url,"wb").write(r.content)

    if motion == "pan_up":
        try:
            cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=3*1280/1.4:h=3*720/1.4:y=t*(in_h-out_h)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=3*1280/1.4:h=3*720/1.4:y=t*(in_h-out_h)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    elif motion == "pan_down":
        try:
            cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v]scale=w=-2:h=3*720,crop=w=3*1280/1.4:h=3*720/1.4:y=(in_h-out_h)-t*(in_h-out_h)/5,scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v]scale=w=-2:h=3*720,crop=w=3*1280/1.4:h=3*720/1.4:y=(in_h-out_h)-t*(in_h-out_h)/5,scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    elif motion == "pan_right":
        try:
            cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=2.6*1280/1.25:h=2.6*720/1.25:x=(in_w-out_w)-t*(in_w-out_w)/5,  scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=2.6*1280/1.25:h=2.6*720/1.25:x=(in_w-out_w)-t*(in_w-out_w)/5,  scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    elif motion == "pan_left":
        try:
            cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=2.6*1280/1.25:h=2.6*720/1.25:x=t*(in_w-out_w)/5,  scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=2.6*1280/1.25:h=2.6*720/1.25:x=t*(in_w-out_w)/5,  scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    elif motion == "rotate_clockwise":
        cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex" + " [0:v]scale=w='if( gt(iw\, ih)\, -2\, 1152.9071700823 )':h='if( gt(iw\,ih)\, 1152.9071700823\, -2  )',rotate=a=0.39269908169872*t/5:c=black:ow=1280:oh=720 " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
        os.system(cmd)

    elif motion == "rotate_anti_clockwise":
        cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex " + " [0:v]scale=w='if( gt(iw\, ih)\, -2\, 1152.9071700823 )':h='if( gt(iw\,ih)\, 1152.9071700823\, -2  )',rotate=a=-0.39269908169872*t/5:c=black:ow=1280:oh=720" + " -c:v h264 -crf 18 -preset veryfast " + vid_out
        os.system(cmd)

    elif motion == "pan_top_right":
        try:
            cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v] scale=w=-2:h=3*720 , crop=w=3*1280/1.4:h=3*720/1.4:y=t*(in_h-out_h)/5:x=(in_w-out_w)-t*(in_w-out_w)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v] scale=w=-2:h=3*720 , crop=w=3*1280/1.4:h=3*720/1.4:y=t*(in_h-out_h)/5:x=(in_w-out_w)-t*(in_w-out_w)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    elif motion == "pan_bottom_right":
        try:
            cmd  = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v]scale=w=-2:h=3*720, crop=w=3*1280/1.4:h=3*720/1.4:y=(in_h-out_h)-t*(in_h-out_h)/5:x=(in_w-out_w)-t*(in_w-out_w)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd  = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v]scale=w=-2:h=3*720, crop=w=3*1280/1.4:h=3*720/1.4:y=(in_h-out_h)-t*(in_h-out_h)/5:x=(in_w-out_w)-t*(in_w-out_w)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    elif motion == "pan_top_left":
        try:
            cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=3*1280/1.4:h=3*720/1.4:y=t*(in_h-out_h)/5:x=t*(in_w-out_w)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex " + " '[0:v] scale=w=-2:h=3*720 , crop=w=3*1280/1.4:h=3*720/1.4:y=t*(in_h-out_h)/5:x=t*(in_w-out_w)/5, scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    elif motion == "pan_bottom_left":
        try:
            cmd = "ffmpeg -y -loop 1 -i " + combined_url + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v]scale=w=-2:h=3*720,crop=w=3*1280/1.4:h=3*720/1.4:y=(in_h-out_h)-t*(in_h-out_h)/5:x=t*(in_w-out_w)/5,scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            if os.system(cmd) != 0:
                raise UserWarning
        except UserWarning:
            filename = str(uuid4())
            con_img = os.path.join(BASE_DIR, "media/images/" + filename + "." + image_url.split(".")[-1])
            cmd1 = "ffmpeg -i " + combined_url + " -vf scale=1280:720 " + con_img
            os.system(cmd1)
            cmd = "ffmpeg -y -loop 1 -i " + con_img + " -ss 0 -t 3 " + " -filter_complex" + " '[0:v]scale=w=-2:h=3*720,crop=w=3*1280/1.4:h=3*720/1.4:y=(in_h-out_h)-t*(in_h-out_h)/5:x=t*(in_w-out_w)/5,scale=w=1280:h=720' " + " -c:v h264 -crf 18 -preset veryfast " + vid_out
            os.system(cmd)
            path_remover(con_img)

    generated_video = open(vid_out, "rb")
    generated_video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".mp4"),
                                                                 created_at=datetime.utcnow())
    generated_video.close()
    path_remover(vid_out)
    path_remover(combined_url)
    message = "scene created successfully"
    return Response({"message": message,
                     "data": os.path.join(BASE_URL, generated_video_file.temp_file.url[1:]),
                     "status":True})