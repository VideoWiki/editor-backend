import os
import urllib.request
import uuid
from moviepy.editor import VideoFileClip
from coutoEditor.global_variable import BASE_URL, BASE_DIR, room_end, dev_end
from library.file_dirs import editor_temp_dir, editor_output_dir
from video.models import ClipRecords
import requests
from .clip_chunks_email_sender import clip_chunk_mail

def split_to_chunk(input_path, mode, email):
    '''
    Method Params:
    input_path: The video file url or directory path file name
    mode: "short" and "long" modes are available which takes a silence of 3 and 5 secs respectively for splitting the video
    Function returns: Clipped videos

    '''

    filename = str(uuid.uuid4())
    uid_dir = filename
    temporary_dir = BASE_DIR + '/' + editor_temp_dir  # editor_temp_dir = media/editor/clip_chunks/temp/"
    output_dir = BASE_DIR + '/' + editor_output_dir + uid_dir + '/'  # editor_output_dir = "media/editor/clip_chunks/"
    silence_file = temporary_dir + filename + "_silence.txt"

    # Check for broken url
    r = requests.get(input_path, stream=True)
    if not r.status_code == 200:
        return "broken url process could not be completed"

    if not os.path.exists(temporary_dir):
        os.mkdir(temporary_dir)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if (os.path.isfile(input_path)):  # todo handle this case
        input_path_vid = BASE_DIR + input_path
        pass
    else:
        ext_name = filename + '_temp_video.mp4'
        ext_path = temporary_dir + ext_name
        urllib.request.urlretrieve(input_path, ext_path)
        input_path_vid = ext_path

    THRESH = "15.72"
    if (mode == 'long'):
        DURATION = "5"
    else:
        DURATION = "3"

    cmd = "ffmpeg -hide_banner -vn -i " + input_path_vid + " -af 'silencedetect=n='" + THRESH + "dB:d=" + DURATION + " -f null - 2>&1 | grep 'silence_end' | awk '{print $5,$8}' > " + silence_file
    os.system(cmd)

    og_vid = VideoFileClip(input_path_vid)
    total_dur = og_vid.duration
    if (os.stat(silence_file).st_size == 0):
        if email == None:
            status_res = "email field was null"
        else:
            send_mail = clip_chunk_mail(email)
            status_res = send_mail
        print("No " + mode + " silences detected")
        output_path = output_dir + "clip_1" + ".webm"
        webm_cmd = "ffmpeg -loglevel panic -i " + input_path_vid + " -c:v libvpx-vp9 -crf 35 -b:v 0 -cpu-used -5 -deadline realtime " + output_path
        os.system(webm_cmd)

        if os.path.exists(input_path_vid):
            os.remove(input_path_vid)
        if os.path.exists(silence_file):
            os.remove(silence_file)

        clip_record_obj = ClipRecords.objects.create(uid=uid_dir)
        if input_path.startswith(room_end) or \
                input_path.startswith(dev_end):  # save the chunks with presentation id
            meeting_id = input_path.split("/")[-2]
            clip_record_obj.meeting_id = meeting_id
            clip_record_obj.is_record = True

        clip_record_obj.save()

        output_url = BASE_URL + editor_output_dir + uid_dir + '/' + "clip_1" + ".webm"
        result_dict = {
            "data": [output_url],
            "uid": clip_record_obj.uid,
            "meeting_id": clip_record_obj.meeting_id,
            "mail": status_res
        }

        return result_dict

    else:
        if email == None:
            status_res = "email field was null"
        else:
            send_mail = clip_chunk_mail(email)
            status_res = send_mail
        video_url_list = []
        count = 0
        silence = open(silence_file, "r", errors='replace')
        silence_list = []

        for line in silence:
            silence_list.append(line.split())

        for i in range(len(silence_list)):
            try:
                sil_dur = float(silence_list[i][1])

                count += 1
                sil_end = float(silence_list[i][0])
                sil_start = sil_end - sil_dur

                if (count == 1):
                    start = 0
                else:
                    prev_dur = float(silence_list[i-1][1])
                    prev_end = float(silence_list[i-1][0])
                    prev_start = prev_end - prev_dur
                    start = prev_start - 0.5

                try:
                    end = sil_start + 0.5
                except:
                    end = sil_start

                temp_path_vid = temporary_dir + filename + "_clip_" + str(count) + ".mp4"
                cmd_clip = "ffmpeg -loglevel panic -i " + input_path_vid + " -ss  " + str(start) + " -to " + str(
                    end) + " -preset ultrafast -c:v libx264 -c:a copy " + temp_path_vid
                os.system(cmd_clip)

                output_path = output_dir + "clip_" + str(count) + ".webm"
                output_url = BASE_URL + editor_output_dir + uid_dir + '/' + "clip_" + str(count) + ".webm"
                video_url_list.append(output_url)

                webm_cmd = "ffmpeg -loglevel panic -i " + temp_path_vid + " -c:v libvpx-vp9 -crf 35 -b:v 0 -cpu-used -5 -deadline realtime " + output_path
                os.system(webm_cmd)

                if (i == len(silence_list) - 1):
                    try:
                        count += 1
                        temp_path_vid = temporary_dir + filename + "_clip_" + str(count) + ".mp4"
                        cmd_clip = "ffmpeg -loglevel panic -i " + input_path_vid + " -ss  " + str(end - 0.5) + " -to " + str(
                                total_dur) + " -preset ultrafast -c:v libx264 -c:a copy " + temp_path_vid
                        os.system(cmd_clip)

                        output_path = output_dir + "clip_" + str(count) + ".webm"
                        output_url = BASE_URL + editor_output_dir + uid_dir + '/' + "clip_" + str(count) + ".webm"
                        video_url_list.append(output_url)

                        webm_cmd = "ffmpeg -loglevel panic -i " + temp_path_vid + " -c:v libvpx-vp9 -crf 35 -b:v 0 -cpu-used -5 -deadline realtime " + output_path
                        os.system(webm_cmd)
                    except:
                        break

            except:
                continue
        if os.path.exists(input_path_vid):
            os.remove(input_path_vid)
        if os.path.exists(silence_file):
            os.remove(silence_file)

        for i in range(1, count + 1):
            temp_path_vid = temporary_dir + filename + "_clip_" + str(i) + ".mp4"
            try:
                os.remove(temp_path_vid)
            except:
                pass

        clip_record_obj = ClipRecords.objects.create(uid=uid_dir)
        if input_path.startswith("https://room.video.wiki/presentation") or \
                input_path.startswith("https://dev.class.video.wiki/presentation"): # save the chunks with presentation id
            meeting_id = input_path.split("/")[-2]
            clip_record_obj.meeting_id = meeting_id
            clip_record_obj.is_record = True

        clip_record_obj.save()

        result_dict = {
            "data": video_url_list,
            "uid": clip_record_obj.uid,
            "meeting_id": clip_record_obj.meeting_id,
            "mail": status_res
        }

        return result_dict

