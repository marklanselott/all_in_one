import aiohttp, json, re, html
from bs4 import BeautifulSoup
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://tmate.cc/'

headers = {
    ":authority": "tmate.cc",
    ":method": "GET",
    ":path": "/",
    ":scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,ru;q=0.5",
    "Priority": "u=0, i",
    "Referer": "https://tmate.cc/",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}


async def main(tiktok_url: str, headers: dict=headers) -> init.response:
    status = False
    data_ = None
    FullReponse = None

    try:
        Content_list = []
        TiktokType = None

        data = {"url": tiktok_url}

        home_url = "https://tmate.cc/"
        post_url = "https://tmate.cc/action"

        async with aiohttp.ClientSession() as session:
            async with session.get(home_url, headers=headers) as response:
                html_ = await response.text()
                soup = BeautifulSoup(html_, 'html.parser')
                hash = soup.find("form", class_ = "form-inline").find_all('input')[1].get("value")
                data['token'] = hash
                headers = {
                    "Cookie": f"session_data={response.cookies.get("session_data").value}",
                    "Origin": "https://tmate.cc",
                    "Priority": "u=1, i",
                    "Referer": "https://tmate.cc/",
                    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                }

                async with session.post(post_url, data=data, headers=headers) as response:
                    FullReponse = json.loads(await response.text())
                    html_ = FullReponse['data']
                    soup = BeautifulSoup(html_, 'html.parser')
                    
                    if '<div class="card">' in html_:
                        TiktokType = init.TiktokType.Photos
                    else:
                        TiktokType = init.TiktokType.Video

                    if TiktokType == init.TiktokType.Photos:
                        photos = soup.find_all("div", class_="card")
                        for photo in photos:
                            Content_list.append(Content(ContentTypes.Photo, photo.find("img").get("src")))
                        
                        Content_list.append(Content(ContentTypes.Audio, soup.find("div", class_="abuttons mb-0").find("a").get("href")))
                    else:
                        links = soup.find("div", class_="abuttons mb-0").find_all("a")
                        
                        Content_list.append(Content(ContentTypes.Audio, links[-1].get("href")))
                        links.pop(-1)
                        for link in links:
                            Content_list.append(Content(ContentTypes.Video, link.get("href")))


                    Preview = soup.find("div", class_="downtmate-left left").find("img").get("src")
                    Caption=html.unescape(soup.find("div", class_="downtmate-left left").find("img").get("alt"))
                    users = re.findall(r'@\w+', Caption)
                    hashtags = re.findall(r'#\w+', Caption)
                    data_ = init.init(FullReponse, TiktokType, Content_list, ExtraOptions=init.init.Additionally(Caption=Caption, Users=users, Hashtags=hashtags, Preview=Preview))






    except: pass
    else: status=True
    return init.response(status, "TMate", data_)
 