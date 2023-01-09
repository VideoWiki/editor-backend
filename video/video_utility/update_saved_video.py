from coutoEditor.settings import BASE_URL, BASE_DIR
from video.models import *
from music_library.models import MusicLib
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .helper_functions import add_scenes_to_video
from .thumbnail_gif import to_thumbnail, to_gif
from django.core.exceptions import ObjectDoesNotExist

def update_video(request):
    save_video_id = request.data["saved_id"]
    video_bin = open(
        os.path.join(
            BASE_DIR,
            request.data["url"].replace(BASE_URL, "")),
        "rb")
    try:
        user_pk = User.objects.get(
            id=request.data["user_id"]
        )
    except ObjectDoesNotExist:
        return JsonResponse({
            'message': "user doesn't exist",
            "status": status.HTTP_400_BAD_REQUEST
        })

    title = request.data["title"]
    description = request.data["description"]
    duration = datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))), "%H:%M:%S").time()
    language = request.data["language"]
    script = request.data["script"]

    # thumbnail
    thumbnail_url = to_thumbnail(
        request.data["url"].replace(BASE_URL, "")
    )
    thumbnail_bin = open(os.path.join(BASE_DIR, thumbnail_url), "rb")
    thumbnail = File(thumbnail_bin, name=thumbnail_url.split('/')[-1])
    # gif null for now
    # gif_url = to_gif(request.data["video"].replace(BASE_URL, ""))
    # gif_bin = open(os.path.join(BASE_DIR, gif_url), "rb")
    # gif = File(gif_bin, name=gif_url.split('/')[-1])
    gif = None
    created_at = datetime.utcnow()
    video_file = File(video_bin, name=request.data["url"].split('/')[-1])
    is_paid = bool(request.data["is_paid"])

    if request.data["bg_music"]["id"] != None:
        bg_music_pk = MusicLib.objects.get(
            id=request.data["bg_music"]["id"]
        )
        bg_music_file = None
    else:
        if request.data["bg_music"]["url"] != None:
            bg_music_file_bin = open(os.path.join(BASE_DIR, request.data["bg_music"]["url"].replace(BASE_URL, "")), "rb")
            bg_music_file = File(bg_music_file_bin, name=request.data["bg_music"]["url"].split('/')[-1])
        else:
            bg_music_file = None
        bg_music_pk = request.data["bg_music"]["id"]

    video = SavedVideo.objects.get(
        id=save_video_id
    ).video
    video.title = title
    video.thumbnail = thumbnail
    video.script = script
    video.bg_music_lib = bg_music_pk
    video.bg_music_file = bg_music_file
    video.gif = gif
    video.video_file = video_file
    video.created_at = created_at
    video.description = description
    video.duration = duration
    video.is_paid = is_paid
    video.language = language
    video.save()
    updated_video_details = Video.objects.get(
        id=video.id
    )
    video_bin.close()
    thumbnail_bin.close()
    # gif_bin.close()
    for tag in request.data["tags"]:
        obj, created = Tags.objects.get_or_create(
            tag_text=tag
        )
        updated_video_details.tags.add(obj.id)

    updated_saved_video = SavedVideo.objects.get(
        id=save_video_id
    )
    # removing the old scene
    all_old_scenes = Scenes.objects.filter(
        saved_video=updated_saved_video.id
    )
    for scene in all_old_scenes:
        old_subtitle = Subtitle.objects.filter(scene=scene)
        old_media = Media.objects.filter(scene=scene)
        old_audio = Audio.objects.filter(scene=scene)
        old_subtitle.delete()
        old_media.delete()
        old_audio.delete()
        scene.delete()

    add_scenes_to_video_res = add_scenes_to_video(
        request.data["scenes"],
        updated_saved_video
    )
    if add_scenes_to_video_res["status"] == 201:
        return Response({
            "message": "video updated successfully.",
            "id": updated_saved_video.id,
            "status": status.HTTP_201_CREATED
        })
    else:
        return Response({
            "message": add_scenes_to_video_res["Message"],
            "status": status.HTTP_400_BAD_REQUEST
        })
