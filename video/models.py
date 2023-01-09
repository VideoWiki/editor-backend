from django.db import models
from django.utils import timezone
from music_library.models import MusicLib
from user.models import User


class Tags(models.Model):
    tag_text = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.tag_text


class Video(models.Model):
    tags = models.ManyToManyField(Tags, blank=True)
    bg_music_lib = models.ForeignKey(MusicLib, on_delete=models.DO_NOTHING, null=True, blank=True)
    bg_music_file = models.FileField(upload_to='saved/%Y/%m/%d/bg_music', blank=True, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    script = models.TextField(null=True, blank=True, default="")
    thumbnail = models.FileField(upload_to='publish/%Y/%m/%d/thumbnails', default=None, null=True, blank=True)
    gif = models.FileField(upload_to='publish//%Y/%m/%d/gifs', default=None, null=True, blank=True)
    video_file = models.FileField(upload_to='publish/%Y/%m/%d/videos', default=None, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.datetime.utcnow, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    duration = models.TimeField(default=timezone.datetime.utcnow, null=True, blank=True)
    language = models.CharField(max_length=50, default="en", null=True, blank=True)
    contributor = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return str(self.title)

class SavedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    video = models.OneToOneField(Video, on_delete=models.DO_NOTHING, null=True, blank=True)
    def __str__(self):
        return str(self.video.title)


class PublishedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # FK?
    is_paid = models.BooleanField(default=False, blank=True, null=True)
    video = models.OneToOneField(Video, on_delete=models.CASCADE, null=True, blank=True)
    saved_video = models.OneToOneField(SavedVideo, on_delete=models.CASCADE, null=True, blank=True)


# <- saved video
# has subtitle and media and audio
class Scenes(models.Model):
    saved_video = models.ForeignKey(SavedVideo, on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=1, null=True, blank=True)
    title = models.TextField(null=True, blank=True, default="")
    # transition type?
    transition = models.CharField(max_length=200, null=True, blank=True)  # todo
    tags = models.ManyToManyField(Tags, blank=True)


# <-scenes
class Subtitle(models.Model):
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE, null=True, blank=True)

    alignment_types = (
        ("left", "left"),
        ("right", "right"),
    )
    alignment = models.CharField(max_length=6, choices=alignment_types, null=True, blank=True)
    font_color = models.CharField(max_length=7, null=True, blank=True)
    background_color = models.CharField(max_length=7, null=True, blank=True)

    text_position_types = (
        ("top", "top"),
        ("center", "center"),
        ("bottom", "bottom")
    )
    text_position = models.CharField(max_length=10, choices=text_position_types, null=True, blank=True)
    text = models.TextField(null=True, blank=True, default="")
    font_style = models.CharField(max_length=50, null=True, blank=True)
    font_size = models.IntegerField(null=True, blank=True)  # ?
    font_type = models.CharField(max_length=50, null=True, blank=True)


# <- scenes
class Media(models.Model):
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE, null=True, blank=True)

    med_types = (
        ("upload", "upload"),
        ("library", "library")
    )
    media_type = models.CharField(max_length=10, choices=med_types, null=True, blank=True)
    media_file = models.FileField(upload_to='scenes/media/%Y/%m/%d', blank=True, null=True)
    source_site = models.CharField(max_length=20,null=True, blank=True)
    lib_media_id = models.IntegerField(null=True, blank=True)

    item_duration = models.TimeField(default=timezone.datetime.utcnow, null=True, blank=True)

    cont_types = (
        ("video", "video"),
        ("image", "image")
    )
    content_type = models.CharField(max_length=10, choices=cont_types, null=True, blank=True)

    animation_type = (
        ("none", "none"),
        ("zoom in", "zoom in"),
        ("zoom out", "zoom out")
    )
    animation = models.CharField(max_length=30, choices=animation_type, null=True, blank=True)


# <- scene
class Audio(models.Model):
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE)
    aud_types = (
        ("upload", "upload"),
        ("narration", "narration")
    )
    audio_type = models.CharField(max_length=20, choices=aud_types, null=True, blank=True)
    audio_file = models.FileField(upload_to='saved/%Y/%m/%d/audio', default=None, null=True)


class Fork(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    published_video = models.ForeignKey(PublishedVideo, on_delete=models.SET_NULL, null=True, blank=True)


class TemporaryFiles(models.Model):
    created_at = models.DateTimeField(default=timezone.datetime.utcnow, null=True, blank=True)
    temp_file = models.FileField(upload_to="temporary/%Y/%m/%d")


class ClipRecords(models.Model):
    meeting_id = models.CharField(max_length=150,null=True, blank=True, default='-1')
    uid = models.UUIDField()
    is_record = models.BooleanField(default=False)