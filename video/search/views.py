# Create your views here.
import urllib.parse
import requests
from django.http import JsonResponse
from googletrans import Translator
from rest_framework.views import APIView


class videoSearch(APIView):

	def post(self, request):
		if request.method == 'POST':
			q = str(request.data['searchQuery'])
			srcLang = str(request.data['srcLang'])
			API_KEY = '14852807-36c181b80405f874cca74a5f7'
			c=0
			d=0
			e=0
			userId=[]
			video_dict={}
			video_dict_sub={}
			translator = Translator()
			transObj = translator.translate(q, dest='en')
			q = transObj.text
			URL = "https://pixabay.com/api/videos/?key="+API_KEY+"&q="+urllib.parse.quote(q)
			r = requests.get(URL)
			r = r.json()
			if r['totalHits'] > 0:
				for hit in r['hits']:
					if hit['user_id'] not in userId:
						img_url = hit['userImageURL']
						video_url = hit['videos']['medium']['url']
						tags = hit['tags']
						transObj = translator.translate(tags, dest=srcLang)
						tags = transObj.text
						current_tag = ""
						if True: #v1 not in tags:
							current_tag = q
							current_tag = current_tag+", "
							transObj = translator.translate(current_tag, dest=srcLang)
							current_tag = transObj.text
						userId.append(hit['user_id'])
						video_dict_sub[d] = [img_url,video_url,tags,current_tag]
						d+=1
						e+=1
				video_dict = video_dict_sub

			return JsonResponse(video_dict)