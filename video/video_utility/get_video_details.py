from video.models import *
from rest_framework.response import Response
from rest_framework import status
from coutoEditor.settings import BASE_URL
import os
from django.http import JsonResponse
from library.video_library.pixabay import get_pixabay_url
from django.core.exceptions import ObjectDoesNotExist

def get_video(
        video_id,
        user
):
    try:
        video_details = Video.objects.get(
            id=int(video_id)
        )
        saved_video_id = video_details.savedvideo.id

        #get video type : fork or save
        try:
            video_type = 'forked'
            fork = Fork.objects.get(
                published_video__saved_video=saved_video_id,
                user_id = user.id
            )
            print(fork)
        except ObjectDoesNotExist:
            video_type = 'saved'

        data = {
            "saved_video_id": saved_video_id,
            "video_type": video_type,
            "user": video_details.savedvideo.user.id,
            "title": video_details.title,
            "description": video_details.description,
            "created_at":video_details.created_at,
            "script": video_details.script,
            "thumbnail": os.path.join(
                BASE_URL,
                video_details.thumbnail.url[1:]
            ),
            "duration": video_details.duration,
            "language":video_details.language,
            "url": os.path.join(
                BASE_URL,
                video_details.video_file.url[1:]
            ),
            "bg_music":{},
            "gif": "",
            "scenes": {},
            "tags": []
        }
        if not video_details.gif:
            data["gif"] = None
        else:
            data["gif"] = os.path.join(
                BASE_URL, video_details.gif.url[1:]
            )

        if not video_details.bg_music_file:
            data["bg_music"]["url"] = None
            if video_details.bg_music_lib:
                data["bg_music"]["id"] = video_details.bg_music_lib.id
                data["bg_music"]["url"] = BASE_URL  + "media/"+ str(MusicLib.objects.get(id = data["bg_music"]["id"]).file)
            else:
                data["bg_music"]["id"] = None
        else:
            data["bg_music"]["url"] = os.path.join(
                BASE_URL,
                video_details.bg_music_file.url[1:]
            )
            data["bg_music"]["id"] = None

        saved_video = SavedVideo.objects.get(
            video=video_id
        )
        all_scenes = Scenes.objects.filter(
            saved_video=saved_video.id
        )
        for scene in all_scenes:
            data["scenes"][str(scene.order)] = {
                "title": scene.title,
                "transition": scene.transition,
                "subtitle": {},
                "media": {},
                "audio": {},
                "keywords": []
            }
            subtitle_info = Subtitle.objects.get(
                scene=scene
            )

            data["scenes"][str(scene.order)]["subtitle"] = {

                "text": subtitle_info.text,
                "style": {
                    "alignment": subtitle_info.alignment,
                    "font_color": subtitle_info.font_color,
                    "background_color": subtitle_info.font_color,
                    "text_position": subtitle_info.text_position,
                    "font_style": subtitle_info.font_style,
                    "font_size": subtitle_info.font_size,
                    "font_type": subtitle_info.font_type
                }
            }

            media_info = Media.objects.get(scene=scene)

            data["scenes"][str(scene.order)]["media"] = {
                "source": media_info.media_type,
                "url": "",
                "source_site": media_info.source_site,
                "lib_media_id": media_info.lib_media_id,
                "duration": media_info.item_duration,
                "type": media_info.content_type,
                "animation": media_info.animation,
            }
            if media_info.media_type == "upload":
                data["scenes"][str(scene.order)]["media"]["url"] = os.path.join(
                    BASE_URL,
                    media_info.media_file.url[1:]
                )

            else:
                id = data["scenes"][str(scene.order)]["media"]["lib_media_id"]
                data["scenes"][str(scene.order)]["media"]["url"] = get_pixabay_url(
                    id,
                    media_info.content_type
                )

            audio_info = Audio.objects.get(scene=scene)
            data["scenes"][str(scene.order)]["audio"] = {
                "source": audio_info.audio_type,
                "url": ""
            }
            if audio_info.audio_file:
                data["scenes"][str(scene.order)]["audio"]["url"] = os.path.join(
                    BASE_URL,
                    audio_info.audio_file.url[1:]
                )
            else:
                data["scenes"][str(scene.order)]["audio"]["url"] = None

            data["scenes"][str(scene.order)]["keywords"] = []
            for tags in scene.tags.all():
                data["scenes"][str(scene.order)]["keywords"].append(tags.tag_text)

        for tags in video_details.tags.all():
            data["tags"].append(tags.tag_text)

        return JsonResponse({
            "data": data,
            "status": status.HTTP_200_OK
        },status=status.HTTP_200_OK)
    except SavedVideo.DoesNotExist:
        return Response({
            "message": "video doesn't exist",
            "status": status.HTTP_404_NOT_FOUND
        },status=status.HTTP_400_BAD_REQUEST)
