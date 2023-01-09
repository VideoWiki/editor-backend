
from video.models import TemporaryFiles
from django.core.exceptions import ObjectDoesNotExist

def temproray_file_save(data):
    return TemporaryFiles.objects.create(**data)

def get_temporary_file(data):
    try:
        return TemporaryFiles.objects.get(data.get('id'))
    except ObjectDoesNotExist as e:
        return None