from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from sentence_detection import views
from .sentence_detection_old import  sd_view
from .tags_detect import tag_suggestor

urlpatterns = [
    path('sentence_detection/', views.SentenceDetection.as_view()),

    path('old',sd_view.SentenceDetectionAPI.as_view()),

    # tags
    path('tags/', tag_suggestor.TagFinder.as_view())

]