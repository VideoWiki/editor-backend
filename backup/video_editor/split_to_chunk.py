import math
import os
import uuid
from datetime import datetime
from shutil import rmtree

import moviepy.editor as mp
import requests
from django.core.files import File
from moviepy.editor import AudioFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment
from pydub.silence import detect_silence
from coutoEditor.global_variable import BASE_URL, BASE_DIR
from video.models import TemporaryFiles


def split_to_chunk_old(video_url, option):
    filename = str(uuid.uuid4())
    chunk_size = 256
    r = requests.get(video_url, stream=True)

    combined_url = os.path.join(BASE_DIR, "media/classroom_record/" + filename + ".mp4")

    with open(combined_url, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
        f.close()

    combined_video_url = os.path.join(BASE_DIR, "media/classroom_record/clip_chunks")
    res_dict = {}
    try:
        rmtree('media/classroom_record/clip_chunks')
    except:
        pass
    if not os.path.exists('media/classroom_record/clip_chunks'):
        os.mkdir("media/classroom_record/clip_chunks")

    option = str(option)

    def match_target_amplitude(sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    audio_file = combined_url.split('.')[0] + '_audio.wav'
    audioclip = AudioFileClip(combined_url)
    num_seconds_video = audioclip.duration
    try:
        audioclip.write_audiofile(audio_file)
        message = str("video has been processed successfully")
    except Exception as e:
        message = ["video has no audio ", e]
        clip = mp.VideoFileClip(combined_url)
        num_seconds_video = clip.duration
        if int(num_seconds_video) <= 20:
            l = [0, int(num_seconds_video)]
        else:
            step = 20
            num_new = int(step * (num_seconds_video // step))
            l = [x for x in range(0, int(num_seconds_video) + 1, step)]
            if l[-1] != num_seconds_video:
                l.append(num_seconds_video)

        path_list = []
        url_list = []
        temp_url_list = []
        for i in range(len(l) - 1):
            ffmpeg_extract_subclip(combined_url, l[i], l[i + 1],
                                   targetname='media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))
            clip = mp.VideoFileClip('media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))
            path_list.append(combined_video_url + "/cut{}.mp4".format(i + 1))
            url_list.append(BASE_URL + 'media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))
            generated_videos = open('media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1), "rb")
            temp_video_file = TemporaryFiles.objects.create(temp_file=File(generated_videos, name=filename + ".mp4"),
                                                            created_at=datetime.utcnow())
            generated_videos.close()
            temp_url_list.append(os.path.join(BASE_URL, temp_video_file.temp_file.url[1:]))
            if os.path.exists(BASE_DIR + 'media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1)):
                os.remove(BASE_DIR + 'media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))

        if os.path.exists(audio_file):
            os.remove(audio_file)

        return temp_url_list

    audio_segment = AudioSegment.from_mp3(audio_file)
    normalized_sound = match_target_amplitude(audio_segment, -16.0)

    if option == 'short':
        silent_data = detect_silence(normalized_sound, min_silence_len=2000, silence_thresh=-16, seek_step=1)

    elif option == 'long':
        silent_data = detect_silence(normalized_sound, min_silence_len=4000, silence_thresh=-16, seek_step=1)

    else:
        # option in milliseconds

        l = [0, int(option), num_seconds_video]
        path_list = []
        for i in range(len(l) - 1):
            ffmpeg_extract_subclip(combined_url, l[i], l[i + 1],
                                   targetname='media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))
            clip = mp.VideoFileClip(combined_video_url + "/cut{}.mp4".format(i + 1))
            path_list.append(combined_video_url + "/cut{}.mp4".format(i + 1))
        return path_list

    l = [0]
    for i in range(len(silent_data)):
        a, b = silent_data[i][0], silent_data[i][1]
        avg = math.floor((a + b) / 2000)
        l.append(avg)

    if l[-1] != num_seconds_video:
        l.append(num_seconds_video)

    for k in range(len(l)):
        for j in range(k + 1, len(l) - 1):
            if l[j] == l[k]:
                del l[j]
    if option == 'long':
        for k in range(3):
            for i in range(len(l)):
                if i < (len(l) - 2):
                    if l[i + 1] - l[i] < 40:
                        del l[i + 1]
    else:
        for k in range(3):
            for i in range(len(l)):
                if i < (len(l) - 2):
                    if l[i + 1] - l[i] < 20:
                        del l[i + 1]
    path_list = []
    url_list = []
    temp_url_list = []
    for i in range(len(l) - 1):
        ffmpeg_extract_subclip(combined_url, l[i], l[i + 1],
                               targetname='media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))
        clip = mp.VideoFileClip('media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))
        path_list.append(combined_video_url + "/cut{}.mp4".format(i + 1))
        url_list.append(BASE_URL + 'media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))
        generated_videos = open('media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1), "rb")
        temp_video_file = TemporaryFiles.objects.create(temp_file=File(generated_videos, name=filename + ".mp4"),
                                                        created_at=datetime.utcnow())
        generated_videos.close()
        temp_url_list.append(os.path.join(BASE_URL, temp_video_file.temp_file.url[1:]))
        if os.path.exists(BASE_DIR + 'media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1)):
            os.remove(BASE_DIR + 'media/classroom_record/clip_chunks' + "/cut{}.mp4".format(i + 1))

    if os.path.exists(audio_file):
        os.remove(audio_file)

    return temp_url_list

