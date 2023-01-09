from django.urls import path
from motions import views

urlpatterns = [
    path('add_motion/', views.ImageVideo.as_view())
]