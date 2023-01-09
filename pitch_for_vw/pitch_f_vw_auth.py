from rest_framework.response import Response
from rest_framework_api_key.models import APIKey
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from video.models import TemporaryFiles
from datetime import datetime
from coutoEditor.global_variable import BASE_DIR
from coutoEditor.global_variable import AWS_LOCATION, \
    AWS_SECRET_ACCESS_KEY, \
    AWS_ACCESS_KEY_ID, \
    AWS_STORAGE_BUCKET_NAME, \
    AWS_BASE_URL
import magic, boto3


class S3VideoUploader(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        # api_key = APIKey.objects.get_from_key(key)
        file = TemporaryFiles.objects.create(
            temp_file=request.data['video'],
            created_at=datetime.utcnow()
        )
        path = BASE_DIR + "/" + file.temp_file.url[1:]
        mimetype = file_path_mime(path)
        name = file.temp_file.url.split("/")[-1]
        s3 = boto3.resource('s3', region_name=AWS_LOCATION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        BUCKET = AWS_STORAGE_BUCKET_NAME
        destination = "pitch_for_vw/media/{}".format(name)
        mimetype = file_path_mime(path)
        s3.Bucket(BUCKET).upload_file(path, destination, ExtraArgs={
            "ContentType": mimetype
        })
        url = AWS_BASE_URL + name
        file.temp_file.delete()
        file.delete()
        return Response({
            "status": True,
            "url": url
        })

def file_path_mime(file_path):
    mime = magic.from_file(file_path, mime=True)
    return mime

