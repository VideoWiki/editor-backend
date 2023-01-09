from django.http import JsonResponse
from rest_framework import status
from user.models import User
from ..models import PublishedVideo
from django.core.exceptions import ObjectDoesNotExist


def publish(request):

    # info
    try:
        user = User.objects.get(
            id=request.data["user_id"]
        )
    except ObjectDoesNotExist:
        return JsonResponse({
            'Message': "user doesn't exist",
            "status": status.HTTP_400_BAD_REQUEST
        })

    is_paid = bool(request.data["is_paid"])

    data = {
        'user': user,
        'is_paid': is_paid,
    }

    pub_video_details = PublishedVideo.objects.create(
        **data
    )

    return {
        "Message": "video  published",
        "id": pub_video_details.id,
        "status": status.HTTP_201_CREATED
    }
