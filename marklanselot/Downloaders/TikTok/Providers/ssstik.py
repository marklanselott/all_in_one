import aiohttp
from bs4 import BeautifulSoup
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes

need_for_selenium = False
home_page = 'https://ssstik.io/en-1'

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,ru;q=0.5",
    "content-length": "64",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "hx-current-url": "https://ssstik.io/en-1",
    "hx-request": "true",
    "hx-target": "target",
    "hx-trigger": "_gcaptcha_pt",
    "origin": "https://ssstik.io",
    "priority": "u=1, i",
    "referer": "https://ssstik.io/en-1",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}


async def main(tiktok_url: str, headers: dict=headers):
    status = False
    data_ = None
    FullReponse = {}
    Content_list = []

    try:
        TiktokType = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url="https://ssstik.io/en-1") as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                code = str(soup.find_all('script')[len(soup.find_all('script'))-2])
                s = code.splitlines()
                for i in s:
                    if "s_tt" in i:
                        code = i.replace(" ", "").split("'")[1]
                        break

                data = {
                    "id": tiktok_url,
                    "locale": "en",
                    "tt": code
                }
                async with session.post("https://ssstik.io/abc?url=dl", data=data, headers=headers) as response:
                    html=await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    FullReponse = html

                    if "slide" in html:
                        TiktokType = init.TiktokType.Photos
                    else:
                        TiktokType = init.TiktokType.Video

                    if TiktokType == init.TiktokType.Photos:
                        photos = soup.find("ul", class_="splide__list").find_all("img")
                        for photo in photos:
                            Content_list.append(Content(ContentTypes.Photo, photo.get("data-splide-lazy")))
                        Content_list.append(Content(ContentTypes.Audio, soup.find("div", class_="result_overlay_buttons").find_all("a")[1].get("href")))
                    else:
                        links = soup.find("div", class_="flex-1 result_overlay_buttons pure-u-1 pure-u-sm-1-2").find_all("a")
                        Content_list.append(Content(ContentTypes.Video, links[0].get("href")))
                        Content_list.append(Content(ContentTypes.Audio, links[-1].get("href")))
        data_ = init.init(FullReponse, TiktokType, Content_list)
                    

    except: pass
    else: status=True
    return init.response(status, "ssstik", data_)

