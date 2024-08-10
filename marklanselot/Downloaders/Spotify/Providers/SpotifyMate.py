from bs4 import BeautifulSoup
import aiohttp
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://spotifymate.com/en'

async def main(track_url: str) -> init.response:
    status = False
    data_ = None
    FullReponse = None
    Content_list = []

    try:
        SongName = None
        Artists = None
        Audio = None
        Photo = None
        data = {"url": track_url}

        home_url = "https://spotifymate.com/en"
        post_url = "https://spotifymate.com/action"

        async with aiohttp.ClientSession() as session:
            async with session.get(home_url) as response:
                html = await response.read()
                soup = BeautifulSoup(html, 'html.parser')

                hash = soup.find("form", class_ = "form-inline").find_all('input')[1]
                param = hash.get('name')
                value = hash.get('value')
                data[param] = value

                async with session.post(post_url, data=data) as response:
                    FullReponse = await response.text()
                    soup = BeautifulSoup(FullReponse, 'html.parser')
                    SongName = soup.find("div", class_="hover-underline").text
                    Artists = soup.find("div", class_="spotifymate-downloader-middle text-center").find("span").text

                    #########
                    Photo = Content(ContentTypes.Photo, soup.find("div", class_="spotifymate-downloader-right is-desktop-only").find_all("a")[1].get("href"))
                    Content_list.append(Photo)

                    Audio = Content(ContentTypes.Audio, soup.find("div", class_="spotifymate-downloader-right is-desktop-only").find_all("a")[0].get("href"))
                    Content_list.append(Audio)

                    #########
        data_ = init.init(FullReponse, SongName, Content_list, ExtraOptions=init.init.Additionally(Artists=Artists))
                
    except: pass
    else: status=True
    return init.response(status, "SpotifyMate", data_)



