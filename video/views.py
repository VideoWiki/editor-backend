import os
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from library.pagination.pagination import CustomPaginator
from library.mailchimp.send_mail import sendMail
from video.serializers.fork_video import ForkVideoSerializer
from video.serializers.publish_video import PublishVideoSerializer
from video.serializers.saved_video import SaveVideoSerializer
from .models import PublishedVideo, User, SavedVideo, Fork, Video
from .video_utility import publish_api, get_video_details, save_video, update_saved_video
from library.model.fork import create_fork
from django.core.exceptions import ObjectDoesNotExist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PublishVideo(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        :param request (video details including save video id if exist)
        :return published video id, message and status
        """

        save_response , status = save_video.save(request)
        if status == 200:
            save_id = save_response["id"]
            video_id = SavedVideo.objects.get(
                id=save_id
            ).video_id
            publish_response = publish_api.publish(request)
            published_id = publish_response["id"]

            if publish_response["status"] == 201:
                # updating published id of saved video
                PublishedVideo.objects.filter(
                    id=published_id
                ).update(
                    video=video_id,
                    saved_video=save_id
                )
                # delete if saved video already exist
                if request.data["saved_id"] != None:
                    SavedVideo.objects.get(
                        id=request.data["saved_id"]
                    ).delete()

                # send published mail
                volunteer_template = "6 Publish Successful"
                subject = "Video Published!"
                user = User.objects.get(id=request.data["user_id"])
                username = user.username
                name = username.split('@')[0]
                global_merge_vars = [
                    {
                        'name': 'NAME',
                        'content': name,
                    }

                ]
                sendMail(volunteer_template, username, name, subject, global_merge_vars)

                # successfully published
                return Response(publish_response)

            else:
                # error in publishing video
                video_id = SavedVideo.objects.get(
                    id=save_id
                ).video_id
                Video.objects.get(
                    id=video_id
                ).delete()

                return Response({
                    "Message": publish_response["Message"],
                    "status": status.HTTP_400_BAD_REQUEST
                })
        else:
            # error in saving video
            return Response({
                "Message": save_response["Message"],
                "status": False
            },status=status.HTTP_400_BAD_REQUEST)


class SaveVideo(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        :param request (video details)
        :return saved video id.
        """

        # for update, save_video_id will come
        if not request.data["saved_id"] == None:
            save_video_id = request.data["saved_id"]
            print(save_video_id,"id")
            return update_saved_video.update_video(request)
        else:
            response_dict, status = save_video.save(request)
            return Response(
                response_dict,
                status=status
            )


class SavedVideoDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        :param request (fork_id, published_video_id or saved video id)
        :return details of saved video
        """
        try:
            fork_id = request.GET.get("fork_id")
            published_id = Fork.objects.get(
                id=fork_id
            ).published_id_id
            video_id = PublishedVideo.objects.get(
                id=published_id
            ).video_id
            return get_video_details.get_video(
                str(video_id),
                request.user
            )
        except:
            pass

        try:
            video_id = PublishedVideo.objects.get(
                id=request.GET.get("published_id")
            ).video_id
            return get_video_details.get_video(
                str(video_id),
                request.user

            )

        except:
            pass

        try:
            save_video_id = request.GET.get("saved_video_id")
            video_id = SavedVideo.objects.get(
                id=save_video_id
            ).video_id
            return get_video_details.get_video(
                str(video_id),
                request.user
            )

        except SavedVideo.DoesNotExist:
            return Response({
                "message": "video doesn't exist",
                "status": False},
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateSavedVideo(APIView):
    def post(self, request):
        '''
        :param request (updated video details including saved video id)
        :return updated saved video id
        '''
        return update_saved_video.update_video(request)


class ForkVideo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        :param request (user and published video id)
        :return fork id.
        """
        user_id = request.data["user_id"]
        publish_video_id = request.data["published_id"]

        try:
            user_id = User.objects.get(
                id = user_id
            )
            publish_video_id = PublishedVideo.objects.get(
                id = publish_video_id
            )
        except ObjectDoesNotExist:
            return Response({
                "message": "user or publish_video_id is invalid !",
                "status": False
            },status=status.HTTP_400_BAD_REQUEST)

        forked_video , message , status_code ,status_bool = create_fork(
            publish_video_id=publish_video_id,
            user_id = user_id
        )
        return Response({
            "message": message,
            "forked_id": forked_video.id,
            "status": status_bool
        },status=status_code)


class UserVideos(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        :param request ( request.user)
        :return saved video, published video and forked video of the user.
        """
        if request.method == 'GET':
            user = request.user

            video_type = request.GET.get("video_type")

            if video_type == 'saved':
                videos = SavedVideo.objects.filter(
                    user=user,
                    video__publishedvideo__isnull=True
                ).order_by('-video__created_at')
                serializer = SaveVideoSerializer

            elif video_type == 'published':
                videos = PublishedVideo.objects.filter(
                    user=user
                ).order_by('-video__created_at')
                serializer = PublishVideoSerializer

            elif video_type == 'forked':
                videos = Fork.objects.filter(
                    user=user
                ).order_by('-published_video__video__created_at')
                serializer = ForkVideoSerializer
            else:
                return Response({
                    "Message": "Invalid video type!",
                    "status": False
                },status=status.HTTP_400_BAD_REQUEST)

            paginator = CustomPaginator()
            response = paginator.generate_response(videos, serializer, request)
            return response


class HomeVidoes(APIView):
    """
    :return list of paginated published video
    """

    def get(self, request):
        if request.method == 'GET':
            published_videos = PublishedVideo.objects.all(
            ).order_by('-video__created_at')
            paginator = CustomPaginator()
            response = paginator.generate_response(
                published_videos,
                PublishVideoSerializer,
                request
            )
            return response
