from PIL import Image
from moviepy.editor import *
from moviepy.video import fx
from coutoEditor.settings import BASE_DIR
import uuid
from ..translation.silence_adder import silence_adder
from library.path_remover import path_remover


def no_motion(videos, width, height):
    # both videos will be combined without any motion
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}'  -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]' -map '[v]' -map '[a]' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def fade(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=fade:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def fadeblack(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=fadeblack:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def fadewhite(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=fadewhite:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def distance(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=distance:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def wipeleft(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=wipeleft:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def wiperight(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=wiperight:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def wipeup(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=wipeup:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def wipedown(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=wipedown:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def slideleft(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=slideleft:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def slideright(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=slideright:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def slideup(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=slideup:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def slidedown(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=slidedown:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def smoothleft(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=smoothleft:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def smoothright(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=smoothright:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def smoothup(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=smoothup:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def smoothdown(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=smoothdown:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def circlecrop(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=circlecrop:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def rectcrop(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=rectcrop:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def circleclose(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=circleclose:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def circleopen(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=circleopen:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def horzclose(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=horzclose:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def horzopen(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=horzopen:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def vertclose(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=vertclose:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def vertopen(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=vertopen:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def diagbl(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=diagbl:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def diagbr(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=diagbr:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def diagtl(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=diagtl:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def diagtr(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=diagtr:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def hlslice(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=hlslice:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def hrslice(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=hrslice:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def vuslice(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=vuslice:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def vdslice(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=vdslice:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def pixelize(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=pixelize:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video


def dissolve(videos, width, height):
    for i in videos:
        if "mp4" in i or i.endswith('.webm') or "webm" in i or i.endswith(".mp4") or "avi" in i or i.endswith(".avi") or "https://player.vimeo.com/" in i:
            pass
        else:
            message = "broken url process could not be completed"
            return message
    filename = str(uuid.uuid4())
    video_1 = videos[0]
    vid = VideoFileClip(video_1)
    video_1_time = vid.duration
    offset = int(video_1_time - 1.5)
    video_2 = videos[1]
    width = width
    height = height
    videos = silence_adder(videos)
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    cmd = "ffmpeg -i '{}' -i '{}' -filter_complex '[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v0];[1:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v1];[v0][v1]xfade=transition=dissolve:duration=1:offset={},format=yuv420p;[0:a][1:a]acrossfade=d=0' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        videos[0], videos[1], width, height, width, height, width, height, width, height, offset, combined_video)
    os.system(cmd)
    for i in videos:
        path_remover(i)
    return combined_video

