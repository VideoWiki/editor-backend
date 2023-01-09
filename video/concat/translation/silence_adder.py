import uuid
import os
from coutoEditor.global_variable import BASE_DIR


def silence_adder(videos):
    l = []
    videos_with_no_audio = []
    index_list = []
    for i in enumerate(videos):
        stream = os.popen(
            "ffmpeg.ffprobe -loglevel error -select_streams a -show_entries stream=codec_type -of csv=p=0 '{}'".format(
                i[1]))
        output = stream.read()
        if len(output) == 0:
            l.append(output)
            index_list.append(i[0])
            videos_with_no_audio.append(i[1])
    silenced_video_list = []
    if len(l) > 0:
        j = 0
        for i in videos_with_no_audio:
            filename = str(uuid.uuid4())
            if i.endswith(".webm"):
                silenced_video_path = os.path.join(BASE_DIR, "media/concatenated-videos/") + filename + ".webm"
                cmd = "ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i '{}' -c:v copy -c:a libopus -shortest {}".format(
                    i, silenced_video_path)
            else:
                silenced_video_path = os.path.join(BASE_DIR, "media/concatenated-videos/") + filename + ".mp4"
                cmd = "ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i '{}' -c:v copy -c:a aac -shortest {}".format(
                    i, silenced_video_path)
            os.system(cmd)
            silenced_video_list.append(i)
            videos[index_list[j]] = silenced_video_path
            j += 1
    return videos

