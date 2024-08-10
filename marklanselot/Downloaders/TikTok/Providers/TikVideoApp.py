from bs4 import BeautifulSoup
import aiohttp, html, re
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://tikvideo.app/en'

async def main(tiktok_url: str, headers: dict=None) -> init.response:
    status = False
    data_ = None
    FullReponse = None
    Content_list = []

    try:
        TiktokType = None

        async with aiohttp.ClientSession() as session:
            data = { "q": tiktok_url, "lang": "en" }
            async with session.post("https://tikvideo.app/api/ajaxSearch", data=data, headers=headers) as response: 
                FullReponse = await response.json()
                html_ = FullReponse['data']
                soup = BeautifulSoup(html_, 'html.parser')

                dl_action = soup.find("div", class_="dl-action").find_all("a")
                Content_list.append(Content(ContentTypes.Audio, dl_action[-1].get("href")))
                dl_action.pop(-1)


                if "photo-list" in html_:
                    TiktokType = init.TiktokType.Photos

                    photos = soup.find("ul", class_="download-box").find_all("img")
                    for photo in photos:
                        Content_list.append(Content(ContentTypes.Photo, photo.get("src")))
                else:
                    TiktokType = init.TiktokType.Video
                    for video in dl_action:
                        Content_list.append(Content(ContentTypes.Video, video.get("href")))

        Preview = soup.find("div", class_="image-tik open-popup").find("img").get("href")
        Caption=html.unescape(str(soup.find("h3").text))
        users = re.findall(r'@\w+', Caption)
        hashtags = re.findall(r'#\w+', Caption)
        
        data_ = init.init(FullReponse, TiktokType, Content_list, ExtraOptions=init.init.Additionally(Caption=Caption, Users=users, Hashtags=hashtags, Preview=Preview))

    except: pass
    else: status=True
    return init.response(status, "TikVideoApp", data_)

