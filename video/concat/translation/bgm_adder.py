from coutoEditor.settings import BASE_DIR
import uuid
import os
from library.bgm_downloader import bgm_downloader


def background_music_adder(bgm_url, final_video_url):
    url = bgm_downloader(bgm_url)
    filename = str(uuid.uuid4())
    if bgm_url.endswith('.mp3') or bgm_url.endswith('.wav'):
        pass
    else:
        message = "broken url process could not be completed"
        return message
    combined_video = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    stream = os.popen("ffmpeg.ffprobe -loglevel error -select_streams a -show_entries stream=codec_type -of csv=p=0 '{}'".format(final_video_url))
    output = stream.read()
    if len(output) == 0:
        cmd = "ffmpeg -i '{}' -stream_loop -1 -i '{}' -vcodec copy -acodec libopus -mapping_family 0 -b:a 96k -shortest -map 0:v:0 -map 1:a:0  {}".format(
        final_video_url, url, combined_video)
        os.system(cmd)
    else:
        cmd = "ffmpeg -i '{}' -stream_loop -1 -i '{}' -vcodec copy -filter_complex amix -acodec libopus -mapping_family 0 -b:a 96k -shortest -map 0:v:0 -map 1:a:0  {}".format(
            final_video_url, url, combined_video)
        os.system(cmd)
    if os.path.exists(url):
        os.remove(url)
    return combined_video
