import aiohttp
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://aaplmusicdownloader.com/'


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
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://aaplmusicdownloader.com/api/applesearch.php?url={track_url}") as response:
                data = await response.json()
                FullReponse['seach'] = {}
                FullReponse['seach'] = data
                SongName=data['name'].replace("&#039;", "")
                AlbumName=data['albumname'].replace("&#039;", "")
                Artists=data['artist'].replace("&#039;", "")

                ###########
                Photo = Content(Type=ContentTypes.Photo, Url=data['thumb'])
                Content_list.append(Photo)
                ###########

                Duration=convert_duration(data['duration'])
                async with session.post("https://aaplmusicdownloader.com/api/composer/swd.php", data={"song_name": data['name'], "artist_name": data['artist'], "url": track_url}) as response:
                    data=await response.json()
                    FullReponse['get_link'] = {}
                    FullReponse['get_link'] = data

                    ###########
                    Audio = Content(Type=ContentTypes.Audio, Url=data['dlink'])
                    Content_list.append(Audio)
                    ###########

                    status=True
        data_ = init.init(FullReponse=FullReponse, SongName=SongName, Content=Content_list, ExtraOptions=init.init.Additionally(Duration=Duration, Artists=Artists, AlbumTitle=AlbumName))

    except: pass
    return init.response(status, "applemusicmp3", data_)