from django.db import models


class MusicLib(models.Model):
    title = models.CharField(max_length=100)
    music_genre = (
        ('ambient', 'Ambient'),
        ('blues', 'Blues'),
        ('bumpers & stingers', 'Bumpers & Stingers'),
        ('chill out', 'Chill Out'),
        ('cinematic', 'Cinematic'),
        ('classical', 'Classical'),
        ('corporate', 'Corporate'),
        ('country', 'Country'),
        ('electronic', 'Electronic'),
        ('folk', 'Folk'),
        ('hip hop', 'Hip Hop'),
        ('holidays & special events', 'Holidays & Special Events'),
        ('horror', 'Horror'),
        ('jazz', 'Jazz'),
        ('kids and family', 'Kids & Family'),
        ('pop', 'Pop'),
        ('religious', 'Religious'),
        ('rhythm & blues', 'Rhythm & Blues'),
        ('rock', 'Rock'),
        ('world', 'World')

    )
    genre = models.CharField(max_length=100, choices=music_genre)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True, null=True, upload_to='music-lib/%Y/%M/%D')

    def __str__(self):
        return self.title
