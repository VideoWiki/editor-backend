import urllib.parse
import requests
from coutoEditor.global_variable import PIXABAY_API_KEY

def get_pixabay_url(
        video_id,
        type
):
    if type == "video":
        URL = "https://pixabay.com/api/videos/?key="+PIXABAY_API_KEY+"&id=" + urllib.parse.quote(str(video_id))
        r = requests.get(URL)
        if r.status_code == 200:
            r = r.json()
            return r['hits'][0]['videos']['tiny']['url']
        else:
            return None

    else:
        URL = "https://pixabay.com/api/?key="+PIXABAY_API_KEY+"&id=" + urllib.parse.quote(str(video_id))
        r = requests.get(URL)
        if r.status_code == 200:
            r = r.json()
            return r["hits"][0]["largeImageURL"]
        else:
            return None
