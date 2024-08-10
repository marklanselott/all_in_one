from bs4 import BeautifulSoup
import aiohttp, json, urllib.parse
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://spotisongdownloader.com/'

def convert_duration(duration: str) -> int:
    hours = 0
    minutes = 0
    seconds = 0
    
    times = duration.split(" ")
    for time in times:
        if "h" in time:
            hours = int(time.replace("h", ""))
        elif "m" in time:
            minutes = int(time.replace("m", ""))
        elif "s" in time:
            seconds = int(time.replace("s", ""))

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds

async def main(track_url: str) -> init.response:
    status = False
    data_ = None
    FullReponse = {}
    Content_list = []

    try:
        SongName = None
        Artists = None
        Audio = None
        Photo = None
        Duration=None
        AlbumName=None
        Date=None
        data = {"url": track_url}

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://spotisongdownloader.com/api/composer/spotify/xsingle_track.php?url={track_url}") as response:
                data = json.loads(str(await response.text()).replace("&#039;", "`"))
                FullReponse['seach'] = {}
                FullReponse['seach'] = data
                SongName=data['song_name']
                AlbumName=data['album_name']
                Artists=data['artist']
                Photo=data['img']

                #########
                Photo = Content(ContentTypes.Audio, data['img'])
                Content_list.append(Photo)
                #########

                Duration=convert_duration(data['duration'])
                Date=data['released']
    
            async with session.post(f"https://members.spotisongdownloader.com/api/composer/spotify/swd.php", data={"song_name": SongName, "artist_name": Artists, "url": track_url}) as response:
                data = await response.json()
  
                #########
                Audio = Content(ContentTypes.Audio, data['dlink'])
                Content_list.append(Audio)
                #########

                FullReponse['get_link'] = {}
                FullReponse['get_link'] = data
                data_ = init.init(FullReponse, SongName, Content_list, ExtraOptions=init.init.Additionally(Duration=Duration, Date=Date, AlbumTitle=AlbumName))

    except: pass
    else: status=True
    return init.response(status, "spotisongdownloader", data_)