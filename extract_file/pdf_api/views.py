from rest_framework.views import APIView
from rest_framework import  status
from rest_framework.response import Response
import  requests

class pdf_api(APIView):

    def get(self, request):
        media_url = request.GET.get('url')
        token  = request.GET.get('bearer_token')
        url = str("{}".format(media_url))


        payload = {}
        headers = {
            'Authorization': 'Bearer {}'.format(str(token))
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return Response({
                            'message': 'pdf downloaded',
                            'status': True,
                            'media_url': response
                            }, status_code= status.HTTP_200_OK)
