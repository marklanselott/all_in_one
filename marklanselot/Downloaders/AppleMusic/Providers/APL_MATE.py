from bs4 import BeautifulSoup
import aiohttp
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes


need_for_selenium = False
home_page = 'https://aplmate.com/'

async def main(track_url: str) -> init.response:
    status = False
    data_ = None
    FullReponse = None
    Content_list = []

    try:

        data = {"url": track_url}

        home_url = "https://aplmate.com/"
        post_url = "https://aplmate.com/action"

        async with aiohttp.ClientSession() as session:
            async with session.get(home_url) as response:
                html = await response.read()
                
                soup = BeautifulSoup(html, 'html.parser')

                hash = soup.find("form", class_ = "form-inline").find_all('input')[1]
                param = hash.get('name')
                value = hash.get('value')
                data[param] = value

                async with session.post(post_url, data=data) as response:
                    FullReponse=await response.text()
                    
                    soup = BeautifulSoup(FullReponse, 'html.parser')
                    SongName = (soup.find("h3").text).replace("\n", "")
                    Artists = soup.find("div", class_="aplmate-downloader-middle text-center").find("span").text
                    
                    ###########
                    Audio = Content(Type=ContentTypes.Audio, Url="https://aplmate.com/" + soup.find("div", class_="aplmate-downloader-right is-desktop-only").find_all("a")[0].get("href"))
                    Photo = Content(Type=ContentTypes.Photo, Url=soup.find("img").get("src"))
                    Content_list.append(Photo)
                    Content_list.append(Audio)
                    ###########

                    status=True
                    data_ = init.init(FullReponse, SongName, Content_list, init.init.Additionally(Artists=Artists))
                    
                    
                    
                    
    
    except: pass
    return init.response(status, "APL_MATE", data_)
