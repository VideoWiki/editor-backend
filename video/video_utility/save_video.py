from coutoEditor.global_variable import BASE_URL,BASE_DIR
from video.models import *
from music_library.models import MusicLib
from django.core.files import File
import os
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .helper_functions import add_scenes_to_video
from .thumbnail_gif import to_thumbnail, to_gif
from library.to_duration import convert_to_duration


def save(request):
    video = open(os.path.join(BASE_DIR, request.data["url"].replace(BASE_URL, "")), "rb")

    try:
        user = User.objects.get(
            id=request.data["user_id"]
        )
    except ObjectDoesNotExist:
        return {
            'Message': "user doesn't exist",
            "status": False
        } , status.HTTP_400_BAD_REQUEST

    title = request.data["title"]
    description = request.data["description"]
    script = request.data["script"]
    duration = convert_to_duration((request.data["duration"]))
    language = request.data["language"]

    # thumbnail
    thumbnail_url = to_thumbnail(request.data["url"].replace(BASE_URL, ""))
    thumbnail_bin = open(os.path.join(BASE_DIR, thumbnail_url), "rb")
    thumbnail = File(thumbnail_bin, name=thumbnail_url.split('/')[-1])
    # gif none for now
    # gif_url = to_gif(request.data["url"].replace(BASE_URL, ""))
    # gif_bin = open(os.path.join(BASE_DIR, gif_url), "rb")
    # gif = File(gif_bin, name=gif_url.split('/')[-1])
    gif = None
    created_at = datetime.utcnow()

    video_file = File(video, name=request.data["url"].split('/')[-1])
    if request.data["bg_music"]["id"] != None:
        try:
            bg_music_pk = MusicLib.objects.get(
                id=request.data["bg_music"]["id"]
            )
            bg_music_file = None
        except ObjectDoesNotExist:
            return {
                "message": 'music library id is invalid !',
                "status": status.HTTP_400_BAD_REQUEST
            },status.HTTP_400_BAD_REQUEST
    else:
        if request.data["bg_music"]["url"] != None:
            bg_music_file_bin = open(
                os.path.join(
                    BASE_DIR,
                    request.data["bg_music"]["url"].replace(BASE_URL, "")),
                    "rb"
            )
            bg_music_file = File(
                bg_music_file_bin,
                name=request.data["bg_music"]["url"].split('/')[-1]
            )
        else:
            bg_music_file = None
        bg_music_pk = request.data["bg_music"]["id"]
    video_data = {
        'title': title,
        'script': script,
        'thumbnail': thumbnail,
        "bg_music_lib": bg_music_pk,
        "bg_music_file": bg_music_file,
        'gif': gif,
        'video_file': video_file,
        'created_at': created_at,
        'description': description,
        'duration': duration,
        'language': language,
    }
    video_details = Video.objects.create(**video_data)
    saved_video_details = SavedVideo.objects.create(
        user_id=user.id,
        video_id=video_details.id
    )
    video.close()
    thumbnail_bin.close()
    # gif_bin.close()
    if request.data["bg_music"]["url"] != None and request.data["bg_music"]["id"]==None:
        bg_music_file_bin.close()

    for tag in request.data["tags"]:
        obj, created = Tags.objects.get_or_create(tag_text=tag)
        video_details.tags.add(obj.id)
    add_scenes_to_video_res = add_scenes_to_video(
        request.data["scenes"],
        saved_video_details
    )
    if add_scenes_to_video_res["status"] == 201:
        return {
            "message": "video saved successfully !",
            "id": saved_video_details.id,
            "status": True
        },status.HTTP_200_OK

    else:
        saved_video_details.delete()
        video_details.delete()
        return {
            "message": add_scenes_to_video_res["Message"],
            "status": False
        },status.HTTP_400_BAD_REQUEST
