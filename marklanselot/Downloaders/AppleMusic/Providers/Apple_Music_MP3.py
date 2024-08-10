import aiohttp
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://apple-music-downloader.com/'

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
        Duration=None
        FullReponse = {
            "get_track": None,
            "create_task": None,
            "generate_download_link": None,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://api.fabdl.com/apple-music/get?url={track_url}") as response:
                data = await response.json()
                SongName=data['result']['name']
                Artists=data['result']['artists']
                Duration=int(data['result']['duration_ms']/1000)

                ###########
                Photo = Content(Type=ContentTypes.Photo, Url=data['result']['image'])
                Content_list.append(Photo)
                ###########

                FullReponse['get_track'] = data
                async with session.get(url=f"https://api.fabdl.com/apple-music/mp3-convert-task/{data['result']['gid']}/{data['result']['id']}") as response:
                    data = await response.json()
                    FullReponse['create_task'] = data
                while True:
                    async with session.get(url=f"https://api.fabdl.com/apple-music/mp3-convert-progress/{data['result']['tid']}/{data['result']['track_id']}") as response:
                        # data = await response.json()
                        # print(data)
                        if data['result']['status'] == 3:
                            data['result']['download_url'] = f"https://api.fabdl.com{data['result']['download_url']}"
                            
                            ###########
                            Audio = Content(Type=ContentTypes.Audio, Url=data['result']['download_url'])
                            Content_list.append(Audio)
                            ###########

                            FullReponse["generate_download_link"] = data
                            status=True
                            break
                        elif data['result']['status'] == -3:
                            break
        
        
        data_ = init.init(FullReponse, SongName, Content_list, init.init.Additionally(Duration=Duration, Artists=Artists))

    except: pass
    return init.response(status, "Apple_Music_MP3", data_)