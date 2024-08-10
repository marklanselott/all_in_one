import json, aiohttp, re, base64
from bs4 import BeautifulSoup
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

home_url = "https://yt5s.biz/ru/youtube-to-mp3"

def get_track_id(yt_url: str) -> str:
    return yt_url.split("=")[1]

def convert_duration(string: str):
    hours, minutes, seconds = map(int, string.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

async def main(yt_url: str) -> init.response: 
    status = False
    data_ = None
    FullReponse = {}
    Content_list = []

    try:
        SongName = None
        Duration = None

        async with aiohttp.ClientSession() as session:
            data = {
                "url": yt_url,
                "ajax": 1,
                "lang": "ru"
            }
            async with session.post("https://yt5s.biz/mates/en/analyze/ajax?retry=undefined&platform=youtube", data=data) as response:
                data = json.loads(await response.text())
                FullReponse['GetInfo'] = {}
                FullReponse['GetInfo'] = data
                html_ = data['result']
                soup = BeautifulSoup(html_, "html.parser")
                Duration = convert_duration((soup.find("p", class_="m-b-0 m-t").text).replace("Duration: ", ""))

                SongName = soup.find("span", id="video_title").text
                Photo = Content(ContentTypes.Photo, soup.find("img", class_="img-thumbnail").get("src"))
                Content_list.append(Photo)

                track_id=get_track_id(yt_url)
                data = {
                    "platform": "youtube",
                    "url": yt_url,
                    "title": SongName,
                    "id": track_id,
                    "ext": "mp3",
                    "note": "mp3-320k",
                    "format": ""
                }
                async with session.post(f"https://yt5s.biz/mates/en/convert?id={track_id}", data=data) as response:
                    data = await response.json()
                    FullReponse['GetLink'] = {}
                    FullReponse['GetLink'] = data
                    Audio = Content(ContentTypes.Audio, data['downloadUrlX'])
                    Content_list.append(Audio)
                    data_ = init.init(FullReponse, SongName, Content_list, ExtraOptions=init.init.Additionally(Duration=Duration))

    except: pass
    else: status = True
    return init.response(status, "yt5s", data_)

