from django.contrib import admin
from .models import Video, PublishedVideo,Tags, SavedVideo, Scenes,Media,Subtitle, Audio, Fork, ClipRecords
# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','title')

@admin.register(PublishedVideo)
class PublishedVideoAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(SavedVideo)
class SavedVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

@admin.register(ClipRecords)
class ClipRecordsAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Fork)
class SavedVideoAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('id',)



@admin.register(Scenes)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id','tag_text')