import os
import uuid
from datetime import datetime
import requests
from django.core.files import File
from django.http import JsonResponse
from requests.exceptions import ConnectionError
from coutoEditor.settings import BASE_URL, BASE_DIR
from library.path_remover import path_remover
# importing all the translation funcs
from video.concat.translation.translation_funcs import no_motion, fade, fadeblack, fadewhite, distance, wipeleft, \
    wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, \
    smoothleft, smoothright, smoothup, smoothdown, circlecrop, rectcrop, circleclose, circleopen, horzclose, horzopen, \
    vertclose, vertopen, diagbl, diagbr, diagtl, \
    diagtr, hlslice, hrslice, vuslice, vdslice, pixelize, dissolve
from video.models import TemporaryFiles
from .translation.bgm_adder import background_music_adder
from .translation.concat_all_videos import concat_all
from .translation.no_motion_finder import no_motion_finder
from .translation.email_sender_funcs import concat_mail, hd_video_start_mail


def merge(v1, v2, motion, width, height):
    videos = [v1, v2]
    if motion == "no_motion":
        return no_motion(videos, width, height)
    elif motion == "fade":
        return fade(videos, width, height)
    elif motion == "fadeblack":
        return fadeblack(videos, width, height)
    elif motion == "fadewhite":
        return fadewhite(videos, width, height)
    elif motion == "distance":
        return distance(videos, width, height)
    elif motion == "wipeleft":
        return wipeleft(videos, width, height)
    elif motion == "wiperight":
        return wiperight(videos, width, height)
    elif motion == "wipeup":
        return wipeup(videos, width, height)
    elif motion == "wipedown":
        return wipedown(videos, width, height)
    elif motion == "slideleft":
        return slideleft(videos, width, height)
    elif motion == "slideright":
        return slideright(videos, width, height)
    elif motion == "slideup":
        return slideup(videos, width, height)
    elif motion == "slidedown":
        return slidedown(videos, width, height)
    elif motion == "smoothleft":
        return smoothleft(videos, width, height)
    elif motion == "smoothright":
        return smoothright(videos, width, height)
    elif motion == "smoothup":
        return smoothup(videos, width, height)
    elif motion == "smoothdown":
        return smoothdown(videos, width, height)
    elif motion == "circlecrop":
        return circlecrop(videos, width, height)
    elif motion == "rectcrop":
        return rectcrop(videos, width, height)
    elif motion == "circleclose":
        return circleclose(videos, width, height)
    elif motion == "circleopen":
        return circleopen(videos, width, height)
    elif motion == "horzclose":
        return horzclose(videos, width, height)
    elif motion == "horzopen":
        return horzopen(videos, width, height)
    elif motion == "vertclose":
        return vertclose(videos, width, height)
    elif motion == "vertopen":
        return vertopen(videos, width, height)
    elif motion == "diagbl":
        return diagbl(videos, width, height)
    elif motion == "diagbr":
        return diagbr(videos, width, height)
    elif motion == "diagtl":
        return diagtl(videos, width, height)
    elif motion == "diagtr":
        return diagtr(videos, width, height)
    elif motion == "hlslice":
        return hlslice(videos, width, height)
    elif motion == "hrslice":
        return hrslice(videos, width, height)
    elif motion == "vuslice":
        return vuslice(videos, width, height)
    elif motion == "vdslice":
        return vdslice(videos, width, height)
    elif motion == "pixelize":
        return pixelize(videos, width, height)
    elif motion == "dissolve":
        return dissolve(videos, width, height)

    return None



def translated_concatenation(
        videos,
        motions,
        width,
        height,
        bgm_url,
        email
):
    if not os.path.exists('media/concatenated-videos/'):
        os.mkdir("media/concatenated-videos/")
    res_dict = {}
    motion_finder = no_motion_finder(motions)
    if "True" in motion_finder:
        final_path = concat_all(videos, width, height, bgm_url, email)
        return final_path
    else:
        pass
    download_path = os.path.join(BASE_DIR, "media/concatenated-videos/")
    if not os.path.exists(os.path.join(BASE_DIR, "media/concatenated-videos/")):
        os.mkdir(os.path.join(BASE_DIR, "media/concatenated-videos/"))
    video_list = []
    for video in videos:
        try:
            r = requests.get(video, stream=True)
            if not r.status_code == 200:
                message = "scene {} has broken url {}".format(videos.index(video) + 1, video)
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
                    url2 = download_path + filename +".webm"
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
            return message, videos, width, height, bgm_url, motions
    if width == '1280' and height =='720':
        send_mail = hd_video_start_mail(email)
    combined_list = []
    v = merge(video_list[0], video_list[1], motions[0], width, height)
    if "broken url process could not be completed" in v:
        for i in video_list:
            path_remover(i)
        message = "broken url process could not be completed"
        return message, videos, width, height, bgm_url, motions
    combined_list.append(v)
    j = 1
    filename = str(uuid.uuid4())
    for i in range(2, len(video_list)):
        v = merge(v, video_list[i], motions[j], width, height)
        if "broken url process could not be completed" in v:
            for i in video_list:
                path_remover(i)
            for i in combined_list:
                path_remover(i)
            message = "broken url process could not be completed"
            return message, videos, width, height, bgm_url, motions
        combined_list.append(v)
        j += 1
    if bgm_url!=None:
        try:
            r = requests.get(bgm_url, stream=True)
            if not r.status_code == 200:
                for i in video_list:
                    path_remover(i)
                for i in combined_list:
                    path_remover(i)
                message = "background music url is broken"
                return message, videos, width, height, bgm_url, motions
            if r.status_code == 200:
                v = background_music_adder(bgm_url, v)
                if "broken url process could not be completed" in v:
                    for i in video_list:
                        path_remover(i)
                    for i in combined_list:
                        path_remover(i)
                    message = "background music url is broken"
                    return message, videos, width, height, bgm_url, motions
        except ConnectionError:
            for i in video_list:
                path_remover(i)
            for i in combined_list:
                path_remover(i)
            message = "broken url process could not be completed"
            return message, videos, width, height, bgm_url, motions
    img_path = os.path.join(BASE_DIR, "media/concatenated-videos/" + str(filename) + ".png")
    cmd = "ffmpeg -i {} -vframes 1 -an -s 1280x720 -ss 5 {}".format(v, img_path)
    os.system(cmd)
    generated_video = open(v, "rb")
    generated_img = open(img_path, "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".webm"),
                                               created_at=datetime.utcnow())
    image_file = TemporaryFiles.objects.create(temp_file=File(generated_img, name=filename + ".png"),
                                                created_at=datetime.utcnow())
    generated_img.close()
    generated_video.close()
    path_remover(img_path)
    path_remover(v)
    for i in video_list:
        path_remover(i)
    for i in combined_list:
        path_remover(i)
    res_dict["image_url"]=os.path.join(BASE_URL,image_file.temp_file.url[1:])
    res_dict["video_url"] = os.path.join(BASE_URL,video_file.temp_file.url[1:])
    if width == '1280' and height =='720':
        url = res_dict['video_url']
        print(url,"a")
        send_mail = concat_mail(email,url)
        status = send_mail
        res_dict["mail"] = status
        return res_dict
    return res_dict


def single_video_concat(
        videos,
        bgm_url,
        width,
        height,
        email
):
    if not os.path.exists('media/concatenated-videos/'):
        os.mkdir("media/concatenated-videos/")
    filename = str(uuid.uuid4())
    download_path = os.path.join(BASE_DIR, "media/concatenated-videos/")
    video_url = videos[0]
    v = video_url
    if "https://player.vimeo.com/" in video_url:
        vurl = download_path + filename + ".mp4"
    else:
        vurl = download_path + filename + "." + video_url.split(".")[-1]
    r = requests.get(video_url, stream=True)
    if r.status_code == 200:
        # This command below will allow us to write the data to a file as binary:
        with open(vurl, 'wb') as f:
            f.write(r.content)
        vlist = []
        if vurl.endswith(".jpg") or video_url.endswith(".png") or video_url.endswith(".jpeg"):
            url2 = download_path + filename +".webm"
            cmd = "ffmpeg -loop 1 -i '{}' -t 5 -vf scale={}:{} ".format(vurl, width, height) + url2
            os.system(cmd)
            path_remover(vurl)
            vlist.append(url2)
            if bgm_url != None:
                bg = requests.get(bgm_url)
                if bg.status_code == 200:
                    url2 = background_music_adder(bgm_url, url2)
                else:
                    return "background music is invalid !"
            filename = str(uuid.uuid4())
            img_path = os.path.join(BASE_DIR, "media/concatenated-videos/" + str(filename) + ".png")
            cmd = "ffmpeg -i {} -vframes 1 -an -s 1280x720 -ss 2 {}".format(url2, img_path)
            os.system(cmd)
            generated_video = open(url2, "rb")
            generated_img = open(img_path, "rb")
            video_file = TemporaryFiles.objects.create(
                temp_file=File(generated_video, name=filename + ".webm"),
                created_at=datetime.utcnow()
            )
            image_file = TemporaryFiles.objects.create(temp_file=File(generated_img, name=filename + ".png"),
                                                       created_at=datetime.utcnow())
            generated_img.close()
            generated_video.close()
            path_remover(img_path)
            path_remover(url2)
            path_remover(vurl)
            for i in vlist:
                path_remover(i)
            res_dict = {}
            res_dict["image_url"] = os.path.join(BASE_URL, image_file.temp_file.url[1:])
            res_dict["video_url"] = os.path.join(BASE_URL, video_file.temp_file.url[1:])
            return JsonResponse({"message": "Successful", 'data': res_dict, 'status': True})
    vlist = []
    if v.endswith(".mp4") or "mp4" in v or "avi" in v or v.endswith(".avi") or v.endswith(".webm") or "https://player.vimeo.com/" in v:
        filename = str(uuid.uuid4())
        converted_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
        cmd = "ffmpeg -i '{}' -vf scale={}:{} -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(v,width,height, converted_video)
        vlist.append(converted_video)
        os.system(cmd)
    if bgm_url != None:
        bg = requests.get(bgm_url)
        if bg.status_code == 200:
            converted_video = background_music_adder(bgm_url, converted_video)
        else:
            return "broken url process could not be completed"
    img_path = os.path.join(BASE_DIR, "media/concatenated-videos/" + str(filename) + ".png")
    cmd = "ffmpeg -i {} -vframes 1 -an -s 1280x720 -ss 5 {}".format(converted_video, img_path)
    os.system(cmd)
    generated_video = open(converted_video, "rb")
    generated_img = open(img_path, "rb")
    video_file = TemporaryFiles.objects.create(temp_file=File(generated_video, name=filename + ".webm"),
                                               created_at=datetime.utcnow())
    image_file = TemporaryFiles.objects.create(temp_file=File(generated_img, name=filename + ".png"),
                                               created_at=datetime.utcnow())
    generated_img.close()
    generated_video.close()
    path_remover(img_path)
    path_remover(converted_video)
    path_remover(vurl)
    for i in vlist:
        path_remover(i)
    res_dict = {}
    res_dict["image_url"] = os.path.join(BASE_URL, image_file.temp_file.url[1:])
    res_dict["video_url"] = os.path.join(BASE_URL, video_file.temp_file.url[1:])
    if width == '1280' and height =='720':
        url = res_dict["video_url"]
        send_mail = concat_mail(email,url)
    return res_dict