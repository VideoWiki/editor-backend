from django.http import JsonResponse
from rest_framework.views import APIView
import requests
import urllib.parse
from coutoEditor.global_variable import PIXABAY_API_KEY1,PIXABAY_API_KEY2,PIXABAY_API_KEY3
import random

class VideoList(APIView):

	def post(self, request):
		if request.method == 'POST':
			q = request.data['keywords']

			c=0
			d=0
			e=0
			userId=[]
			video_dict={}
			image_dict={}
			video_dict_sub={}
			video_list_sub = []
			image_list_sub = []
			for k,v in q.items():
				for v1 in v:
					kl = [PIXABAY_API_KEY1, PIXABAY_API_KEY2, PIXABAY_API_KEY3]
					key = random.choice(kl)
					print(key, "lll")
					URL = "https://pixabay.com/api/videos/?key="+key+"&q="+urllib.parse.quote(str(v1))
					r = requests.get(URL)
					r = r.json()
					print(r)
					if not 'totalHits' in r:
						print("Trrure")
						break
					if r['totalHits'] > 0:
						for hit in r['hits']:
							id = hit["id"]
							if hit['user_id'] not in userId and e < 1:
								img_url = hit['userImageURL']
								video_url = hit['videos']['tiny']['url']
								tags = hit['tags']
								if True:
									current_tag = str(v1)
								userId.append(hit['user_id'])

								dic = {"id":id,"thumbnail":img_url,"url":video_url,"tags":tags,"current_tag":current_tag}
								video_list_sub.append(dic)

								d+=1
								e+=1
						e = 0
					else:
						#default links will be generated when no videos are found
						video_dict_sub[d]=["https://oldweb.dyu.edu.tw/english/design/no-video.gif","https://oldweb.dyu.edu.tw/english/design/no-video.gif","",""]
					URL = "https://pixabay.com/api/?key="+key+"&q="+urllib.parse.quote(str(v1))
					r = requests.get(URL)
					r = r.json()
					if 'totalHits' in r:
						if r['totalHits'] > 0:
							for hit in r['hits']:
								dic = {"id":hit["id"],"url":hit["largeImageURL"],"tags":hit["tags"],"current_tag":v1}
								image_list_sub.append(dic)
								break
					else:
						break


				video_dict[c] = video_list_sub
				if len(image_list_sub)!=0:
					image_dict[len(image_dict)]=image_list_sub

				c+=1
				video_list_sub, image_list_sub = [], []
				d=0
			return JsonResponse({"videos":video_dict,"images":image_dict})
