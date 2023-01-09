import os
import uuid
from coutoEditor.settings import BASE_DIR

def no_motion_concat(video_list, width, height):
    filename = str(uuid.uuid4())
    output_video_path = os.path.join(BASE_DIR, "media/concatenated-videos/" + filename + ".webm")
    list1 = []
    for i in video_list:
        x = "-i '{}' ".format(i)
        list1.append(x)
    s1 = ""
    for i in list1:
        s1 += i
    list2 = []
    for i in range(len(video_list)):
        x = "[{}:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1,setsar=1,fps=30,format=yuv420p[v{}];".format(
            i, width, height, width, height, i)
        list2.append(x)
    s2 = ""
    for i in list2:
        s2 += i
    s3 = ""
    for i in range(len(video_list)):
        x = "[v{}][{}a]".format(i, i)
        s3 += x
    cmd = "ffmpeg {} -filter_complex '{}{}concat=n={}:v=1:a=1[v][a]' -map '[v]' -map '[a]' -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus -deadline realtime -cpu-used 8 {}".format(
        s1, s2, s3, len(list1), output_video_path)
    os.system(cmd)
    return output_video_path





