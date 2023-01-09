import requests
import requests.status_codes
from coutoEditor.settings import BASE_DIR
import os
import uuid

def bgm_downloader(bgm_url):
    download_path = os.path.join(BASE_DIR, "media/concatenated-videos/")
    filename = str(uuid.uuid4())
    url = download_path + filename + "." + bgm_url.split(".")[-1]
    bgm = requests.get(bgm_url)
    if bgm.status_code == 200:
        with open(url, 'wb') as f:
            f.write(bgm.content)
        f.close()
        return url
