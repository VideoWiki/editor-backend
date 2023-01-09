from django.urls import path
from video.views import PublishVideo, SavedVideoDetails, SaveVideo, ForkVideo, \
    UserVideos, UpdateSavedVideo, HomeVidoes
from video.upload_media import FileUploadView
from video.editor.views import caption, video_chunks, sil_vid, trim, speed_up_video, crop_video, speed_up_vid_qcl
from video.list import vl_api
from video.concat.views import VideoPreviewMaker
from video.subtitle.views import videoScript, videoScript_mp4
from video.search.vs_api import VideoSearchAPI
from video.audio_merge.views import AudioVideoMerge, AudioVideoMerge_mp4


urlpatterns = [
    path('publish_video/', PublishVideo.as_view()),
    path('save_video/', SaveVideo.as_view()),
    path(r'video_details/', SavedVideoDetails.as_view()),
    path('update_video/', UpdateSavedVideo.as_view()),
    path('fork_video/', ForkVideo.as_view()),
    path('user_videos/', UserVideos.as_view()),
    path('home_videos/', HomeVidoes.as_view()),
    path('upload_media/', FileUploadView.as_view()),

    # editor
    path('get_subtitles/', caption.as_view()),
    path('create_chunks/', video_chunks.as_view()),
    path('remove_audio/', sil_vid.as_view()),
    path('trim_video/', trim.as_view()),

    # list
    path('media_list/', vl_api.VideoList.as_view()),

    # concat
    path('video_concat/', VideoPreviewMaker.as_view()),

    # subtitle
    path('add_subtitle_webm/', videoScript.as_view()),
    path('add_subtitle/', videoScript_mp4.as_view()),

    # search
    path('media_search/', VideoSearchAPI.as_view()),

    # audio video merge
    path('audio_video_merge_webm/', AudioVideoMerge.as_view()),
    path('audio_video_merge/', AudioVideoMerge_mp4.as_view()),

    # speed up video
    path('speed_up_video/', speed_up_video.as_view()),
    path('speed_up_vid/', speed_up_vid_qcl.as_view()),

    # crop video
    path('crop_video/', crop_video.as_view())
]
