from django.contrib import admin
from .models import MusicLib

# Register your models here.

@admin.register(MusicLib)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'file')
    ordering = ('id',)



