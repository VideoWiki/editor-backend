from django.urls import path, include
from extract_file.views import ExtractDetailFromUrl, ExtractDetailFromFile
from extract_file.pdf_api.views import pdf_api


urlpatterns = [
    path(r'extract_info_url/', ExtractDetailFromUrl.as_view()),
    path(r'extract_info_file/', ExtractDetailFromFile.as_view()),
    path('pdf_downloader/', pdf_api.as_view())
]

