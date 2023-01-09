from video.models import Fork
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


def create_fork(
        publish_video_id,
        user_id
):
    try:
        fork =  Fork.objects.get(
            published_video=publish_video_id,
            user = user_id
        ) , 'user already forked this video !',\
                status.HTTP_400_BAD_REQUEST , False
        return fork
    except ObjectDoesNotExist:
        return Fork.objects.create(
            published_video=publish_video_id,
            user = user_id
        ) , "forked successfully !" ,\
               status.HTTP_200_OK , True