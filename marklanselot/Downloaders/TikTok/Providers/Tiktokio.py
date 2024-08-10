import aiohttp, re, html
from bs4 import BeautifulSoup
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://tiktokio.com/'



async def main(tiktok_url: str) -> init.response:
    status = False
    data_ = None
    FullReponse = {}

    try:
        TiktokType = None
        Content_list = []
        Caption=None
        users = None
        hashtags = None
        data = {"vid": tiktok_url}

        home_url = "https://tiktokio.com/"
        post_url = "https://tiktokio.com/api/v1/tk-htmx"

        async with aiohttp.ClientSession() as session:
            async with session.get(home_url) as response:
                html_ = await response.text()
                soup = BeautifulSoup(html_, 'html.parser')
                
                hash = soup.find("input", type = "hidden").get("value")
                data['prefix'] = hash
                
                async with session.post(post_url, data=data) as response:
                    html_=await response.text()
                    soup = BeautifulSoup(html_, 'html.parser')
                    FullReponse=html_

                    if '<div class="row">' in html_:
                        TiktokType = init.TiktokType.Photos
                    else: 
                        TiktokType = init.TiktokType.Video
                    
                    if TiktokType == init.TiktokType.Photos:
                        Content_list.append(Content(ContentTypes.Audio, soup.find_all("div", class_="tk-down-link")[-2].find("a").get("href")))

                        photos = soup.find_all("div", class_="col-12 col-md-4 download-item mt-3")
                        
                        for photo in photos:
                            Content_list.append(Content(ContentTypes.Photo, photo.find("img").get("src")))
                    else:
                        Caption=html.unescape(str(soup.find("h2").text))
                        users = re.findall(r'@\w+', Caption)
                        hashtags = re.findall(r'#\w+', Caption)

                        donload_links = soup.find_all("div", class_="tk-down-link")
                        donload_links.pop(-1)
                        Content_list.append(Content(ContentTypes.Audio, donload_links[-1].find("a").get("href")))
                        donload_links.pop(-1)

                        for link in donload_links:
                            Content_list.append(Content(ContentTypes.Video, link.find("a").get("href")))

        data_ = init.init(FullReponse, TiktokType, Content_list, ExtraOptions=init.init.Additionally(Caption=Caption, Users=users, Hashtags=hashtags))




    except: pass
    else: status=True
    return init.response(status, "Tiktokio", data_)
