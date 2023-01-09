import requests
from coutoEditor.settings import BASE_DIR, BASE_URL
import os
import uuid
from .ffmpeg import no_motion_concat
from video.models import TemporaryFiles
from django.core.files import File
from datetime import datetime
from library.path_remover import path_remover
from requests.exceptions import ConnectionError
from .bgm_adder import background_music_adder
from .email_sender_funcs import concat_mail, hd_video_start_mail

def concat_all(videos, width, height, bgm_url, email):
    res_dict = {}
    video_list = []
    combined_videos = []
    download_path = os.path.join(BASE_DIR, "media/concatenated-videos/")
    for video in videos:
        try:
            r = requests.get(video, stream=True)
            if not r.status_code == 200:
                message = "scene {} has broken url {}".format(videos.index(video)+1, video)
                motions = ["no_motion"]
                for i in video_list:
                    path_remover(i)
                return message, videos, width, height, bgm_url, motions
            if r.status_code == 200:
                if video.endswith(".jpg") or video.endswith(".png") or video.endswith(".jpeg"):
                    filename = str(uuid.uuid4())
                    url = download_path + filename + "." + video.split(".")[-1]
                    with open(url, 'wb') as f:
                        f.write(r.content)
                    filename = str(uuid.uuid4())
                    url2 = download_path + filename + ".webm"
                    cmd = "ffmpeg -loop 1 -i '{}' -t 5 -vf scale={}:{} ".format(url, width, height) + url2
                    os.system(cmd)
                    path_remover(url)
                    path_remover(video)
                    video_list.append(url2)
                else:
                    video_list.append(video)
        except ConnectionError:
            for i in video_list:
                path_remover(i)
            message = "broken url process could not be completed"
            motions = ["no_motion"]
            return message, videos, width, height, bgm_url, motions
    if width == '1280' and height =='720':
        send_mail = hd_video_start_mail(email)
    filename = str(uuid.uuid4())
    l = []
    videos_with_no_audio = []
    index_list = []
    for i in enumerate(video_list):
        stream = os.popen(
            "ffmpeg.ffprobe -loglevel error -select_streams a -show_entries stream=codec_type -of csv=p=0 '{}'".format(
                i[1]))
        output = stream.read()
        if len(output)==0:
            l.append(output)
            index_list.append(i[0])
            videos_with_no_audio.append(i[1])
    silenced_video_list = []
    if len(l) >0:
        j=0
        for i in videos_with_no_audio:
            filename = str(uuid.uuid4())
            if i.endswith(".webm"):
                silenced_video_path = os.path.join(BASE_DIR, "media/concatenated-videos/") + filename + ".webm"
                cmd = "ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i '{}' -c:v copy -c:a libopus -shortest {}".format(
                    i, silenced_video_path)
            else:
                silenced_video_path = os.path.join(BASE_DIR, "media/concatenated-videos/") + filename +".mp4"
                cmd = "ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i '{}' -c:v copy -c:a aac -shortest {}".format(
                    i, silenced_video_path)
            os.system(cmd)
            silenced_video_list.append(i)
            video_list[index_list[j]] = silenced_video_path
            j+=1
    output_video_path = no_motion_concat(video_list, width, height)
    combined_videos.append(output_video_path)
    if bgm_url != None:
        try:
            r = requests.get(bgm_url, stream=True)
            if not r.status_code == 200:
                for i in video_list:
                    path_remover(i)
                    path_remover(output_video_path)
                    for i in silenced_video_list:
                        path_remover(i)
                    message = "background music url is broken"
                    motions = ["no_motion"]
                    return message, videos, width, height, bgm_url, motions
            if r.status_code == 200:
                output_video_path = background_music_adder(bgm_url, output_video_path)
                if "broken url process could not be completed" in output_video_path:
                    for i in video_list:
                        path_remover(i)
                    path_remover(output_video_path)
                    for i in combined_videos:
                        path_remover(i)
                    message = "background music url is broken"
                    motions = ["no_motion"]
                    return message, videos, width, height, bgm_url, motions
        except ConnectionError:
            for i in video_list:
                path_remover(i)
            path_remover(output_video_path)
            message = "broken url process could not be completed"
            motions = ["no_motion"]
            return message, videos, width, height, bgm_url, motions
    img_path = os.path.join(BASE_DIR, "media/concatenated-videos/" + str(filename) + ".png")
    cmd = "ffmpeg -i {} -vframes 1 -an -s 1280x720 -ss 5 {}".format(output_video_path, img_path)
    os.system(cmd)
    generated_video = open(output_video_path, "rb")
    generated_img = open(img_path, "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".webm"),
                                                   created_at=datetime.utcnow())
    image_file = TemporaryFiles.objects.create(temp_file=File(generated_img, name=filename + ".png"),
                                                   created_at=datetime.utcnow())
    generated_video.close()
    generated_img.close()
    path_remover(output_video_path)
    for i in silenced_video_list:
        path_remover(i)
    for i in combined_videos:
        path_remover(i)
    path_remover(img_path)
    for i in video_list:
        path_remover(i)
    res_dict["image_url"] = os.path.join(BASE_URL, image_file.temp_file.url[1:])
    res_dict["video_url"] = os.path.join(BASE_URL, video_file.temp_file.url[1:])
    if width == '1280' and height == '720':
        url = res_dict['video_url']
        send_mail = concat_mail(email,url)
        response = send_mail
        res_dict["mail"]= response
        return res_dict
    return res_dict

