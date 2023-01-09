from django.urls import path

from backup.keywordExtraction import tag_suggestor, views

urlpatterns = [
    path('', views.KeywordExtraction.as_view()),
    path('tags', tag_suggestor.TagFinder.as_view())
]