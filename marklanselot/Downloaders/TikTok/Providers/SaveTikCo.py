import aiohttp, html, re
from bs4 import BeautifulSoup
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://savetik.co/en2'

async def main(tiktok_url: str, headers: dict=None) -> init.response:
    status = False
    data_ = None
    FullReponse = {}
    Content_list = []
    

    try:
        TiktokType = None
        async with aiohttp.ClientSession() as session:
            data = { "q": tiktok_url, "lang": "en" }
            async with session.post("https://savetik.co/api/ajaxSearch", data=data, headers=headers) as response: 
                data=await response.json()
                html_ = data['data']
                photos_links=data
                soup = BeautifulSoup(html_, 'html.parser')
                download_links = soup.find("div", class_="dl-action").find_all("a")
                Audio = Content(ContentTypes.Audio, download_links[len(download_links)-1].get("href"))
                Content_list.append(Audio)
                if "Render Video" in html_:
                    TiktokType = init.TiktokType.Photos
                else:
                    TiktokType = init.TiktokType.Video

                if TiktokType == init.TiktokType.Video:
                    download_links.pop()
                    for link in download_links:
                        Content_list.append(Content(ContentTypes.Video, link.get("href")))
                else:
                    photos_links = soup.find_all("img")
                    photos_links.pop(0)

                    for photo_link in photos_links:
                        Content_list.append(Content(ContentTypes.Photo, photo_link.get("src")))

                Preview = soup.find("div", class_="image-tik open-popup").find("img").get("src")
                Caption=html.unescape(str(soup.find("h3").text))
                users = re.findall(r'@\w+', Caption)
                hashtags = re.findall(r'#\w+', Caption)


                data_ = init.init(FullReponse, TiktokType, Content_list, ExtraOptions=init.init.Additionally(Caption=Caption, Users=users, Hashtags=hashtags, Preview=Preview))





    
    except: pass
    else: status=True
    return init.response(status, "SaveTikCo", data_)

