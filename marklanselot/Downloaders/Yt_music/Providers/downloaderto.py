import asyncio, aiohttp, re, base64
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

home_url = "https://downloaderto.com/ruwq/"

def find_token_api(html: str) -> str:
    pattern = r"&api=[^\s&]+"
    token = re.findall(pattern, html)[0]
    return token

async def main(yt_url: str) -> init.response: 
    status = False
    data_ = None
    FullReponse = {}
    Content_list = []

    try:
        Photo = None
        Audio = None
        SongName = None

        async with aiohttp.ClientSession() as session:
            async with session.get(home_url) as response:
                html = await response.text()
                token = find_token_api(html)
                
                audio_formats = [
                    "m4a",
                    "mp3",
                    "webm",
                    "aac",
                    "flac",
                    "opus",
                    "ogg",
                    "wav"
                ]

                video_formats = [
                    "360",
                    "480",
                    "720",
                    "1080",
                    "1440",
                    "4k",
                ]
                
                format = "m4a"
                get_video_url = f"https://ab.cococococ.com/ajax/download.php?copyright=0&format={format}&url={yt_url}{token}"
                async with session.get(get_video_url) as response:
                    data = await response.json()
                    FullReponse['Get_Song_Dict'] = {}
                    FullReponse['Get_Song_Dict'] = data
                    SongName = data['title']
                    Photo = Content(Type=ContentTypes.Photo, Url=data['info']['image'])
                    Content_list.append(Photo)
                    FullReponse['Get_Song_html'] = {}
                    FullReponse['Get_Song_html'] = base64.b64decode(data['content']).decode('utf-8')
                    
                    html_base64 = data['content']
                    decoded_bytes = base64.b64decode(html_base64)
                    html_str = decoded_bytes.decode('utf-8')
                    FullReponse['ResponseHTML'] = {}
                    FullReponse['ResponseHTML'] = html_str
                    FullReponse['EndResponse'] = {}
                    progress = 0
                    progress_url = f"https://p.oceansaver.in/ajax/progress.php?id={data['id']}"
                    while progress != 1000:
                        async with session.get(progress_url) as response:
                            data = await response.json()
                            if data['progress'] == 1000:
                                FullReponse['EndResponse']=data
                                Audio = Content(Type=ContentTypes.Audio, Url=data['download_url'].replace("\\", ""))
                                Content_list.append(Audio)
                            progress=data['progress']
                            await asyncio.sleep(1)
        data_ = init.init(FullReponse, SongName, Content_list)
    except: pass
    else: status = True
    return init.response(status, "downloaderto", data_)




