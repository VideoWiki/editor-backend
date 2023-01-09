from django.urls import path
from .pitch_f_vw_auth import S3VideoUploader
urlpatterns = [
    path('upload/video/', S3VideoUploader.as_view()),
]