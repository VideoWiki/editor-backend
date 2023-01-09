import os
from django.core.files import File
from rest_framework import status
from coutoEditor.global_variable import BASE_URL
from library.to_duration import convert_to_duration
from video.models import *
from video.serializers.media import MediaSerializer, AudioSerializer
from video.serializers.saved_video import SceneSerializer, SubtitleSerializer
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# subtitle one_to_one scene
def add_subtitle_to_scene(
        subtitle,
        scene
):
    subtitle_data = {
        "scene": scene.id,
        "alignment": subtitle["style"]["alignment"],
        "font_color": subtitle["style"]["font_color"],
        "background_color": subtitle["style"]["background_color"],
        "text_position": subtitle["style"]["text_position"],
        "text": subtitle["text"],
        "font_style": subtitle["style"]["font_style"],
        "font_size": subtitle["style"]["font_size"],
        "font_type": subtitle["style"]["font_type"],
    }

    deserialized_subtitle = SubtitleSerializer(
        data=subtitle_data
    )
    if deserialized_subtitle.is_valid():
        saved_subtitle = deserialized_subtitle.save()

        return {
            "message": "subtitle added to scene",
            "status": status.HTTP_201_CREATED
        }
    else:
        return {
            "message": deserialized_subtitle.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }

#media  one to one to scene
def add_media_to_scene(media, scene):
    item_duration = convert_to_duration(media["duration"])

    media_data = {
        "scene": scene.id,
        "media_type": media["source"],
        "media_file": "",
        "source_site": "",
        "lib_media_id": "",
        "item_duration": item_duration,
        "content_type": media["type"],
        "animation": media["animation"]
    }

    if media["source"] == "upload":
        bin_med_file = open(
            os.path.join(
                BASE_DIR,
                media["url"].replace(BASE_URL, "")
            ), "rb")
        media_file = File(
            bin_med_file,
            name=media["url"].split('/')[-1]
        )
        media_data["media_file"] = media_file
        media_data["source_site"] = media["source_site"]
        media_data["lib_media_id"] = media["lib_media_id"]

    else:
        media_data["media_file"] = None
        media_data["source_site"] = media["source_site"]
        media_data["lib_media_id"] = media["lib_media_id"]


    deserialized_media = MediaSerializer(
        data=media_data
    )
    if deserialized_media.is_valid():
        saved_media = deserialized_media.save()
        if media["source"] == "upload":
            bin_med_file.close()
        return {
            "message": "media added to scene",
            "status": status.HTTP_201_CREATED
        }
    else:
        if media["source"] == "upload":
            bin_med_file.close()
        return {
            "message": deserialized_media.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }

# audio one_to_one scene
def add_audio_to_scene(audio, scene):

    if audio["url"] != None:
        bin_aud_file = open(
            os.path.join(
                BASE_DIR,
                audio["url"].replace(BASE_URL, "")
            ),"rb")
        audio_file = File(
            bin_aud_file,
            name=audio["url"].split('/')[-1]
        )
    else:
        audio_file = None

    audio_data = {
        "scene": scene.id,
        "audio_type": audio["source"],
        "audio_file": audio_file
    }

    deserialized_audio = AudioSerializer(data=audio_data)
    if deserialized_audio.is_valid():
        saved_audio = deserialized_audio.save()
        if audio["url"] != None:
            bin_aud_file.close()
        return {
            "message": "Audio added to scene",
            "status": status.HTTP_201_CREATED
        }

    else:
        if audio["url"] != None:
            bin_aud_file.close()
        return {
            "message": deserialized_audio.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }

#scene  many to one to video
def add_scenes_to_video(
        scenes,
        video
):
    for i in scenes:
        scene_data = {
            "order": int(i),
            "title": scenes[i]["title"],
            "transition": scenes[i]["transition"],
            "saved_video": video.id
        }
        deserialized_scene = SceneSerializer(data=scene_data)

        if deserialized_scene.is_valid():
            saved_scene = deserialized_scene.save()
            scenes_details = Scenes.objects.get(id=saved_scene.id)

            for tag in scenes[i]["keywords"]:
                obj, created = Tags.objects.get_or_create(tag_text=tag)
                scenes_details.tags.add(obj.id)

            subtitle_response = add_subtitle_to_scene(
                scenes[i]["subtitle"],
                scenes_details
            )

            if subtitle_response["status"] != 201:
                scenes_details.delete()
                return subtitle_response

            media_response = add_media_to_scene(
                scenes[i]["media"],
                scenes_details
            )

            if media_response["status"] != 201:
                scenes_details.delete()
                return media_response

            add_audio_response = add_audio_to_scene(
                scenes[i]["audio"],
                scenes_details
            )

            if add_audio_response["status"] != 201:
                scenes_details.delete()
                return add_audio_response


        else:
            return {
                "message": deserialized_scene.errors,
                "status": status.HTTP_400_BAD_REQUEST
            }

    return {
        "message": "scenes created!",
        "status": status.HTTP_201_CREATED
    }
