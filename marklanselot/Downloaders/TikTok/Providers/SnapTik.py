import aiohttp, re, subprocess, os, uuid, html
from bs4 import BeautifulSoup
from . import init
from ...Content import init as Content
from ...Content import Types as ContentTypes


need_for_selenium = False
home_page = 'https://snaptik.app/en1'
need_install_node = True


async def main(tiktok_url: str) -> init.response:
    status = False
    data_ = None
    FullReponse = {}
    Content_list = []
        
    try:
        TiktokType = None

        async with aiohttp.ClientSession() as session:
            async with session.get(url='https://snaptik.app/en1') as response:
                html_ = await response.text()
                soup = BeautifulSoup(html_, "html.parser")
                token = soup.find("div", class_="is-relative").find_all("input")[2].get("value")
                cookies = session.cookie_jar.filter_cookies('https://snaptik.app/en1')
                cookies_dict = {cookie.key: cookie.value for cookie in cookies.values()}
                async with session.post("https://snaptik.app/abc2.php", data={"url": tiktok_url, "lang": "en1", "token": token}, cookies=cookies_dict) as response:
                    js_file = f'{uuid.uuid4().hex}.js'
                    def remove_first_and_last_char(s):
                        if len(s) <= 2: return ''
                        return s[1:-1]

                    a = await response.text()
                    with open(js_file, 'w', encoding="utf-8") as file: file.write(a)
                    result = subprocess.run(['node', js_file], capture_output=True, text=True, encoding='utf-8', errors='replace')
                    os.remove(js_file)
                    result = result.stderr.replace('$("#download").innerhtml_ = ', "<start>").replace('; $(".contents")', "<end>").split("<start>")[0].split("<end>")[0].replace("\\", "")
                    html_ = remove_first_and_last_char(result)
                    FullReponse['low'] = {}
                    FullReponse['low'] = html_
                    soup = BeautifulSoup(html_, "html.parser")
                    

                    if "photo" in html_:
                        TiktokType = init.TiktokType.Photos
                        photos = soup.find_all("div", class_="photo")
                        for photo in photos:
                            Content_list.append(Content(ContentTypes.Photo, photo.find("img").get("src")))
                    else: 
                        TiktokType = init.TiktokType.Video

                    if TiktokType == init.TiktokType.Video:
                        Content_list.append(Content(ContentTypes.Video, soup.find("a").get("href")))
                        hd_url = f"https://snaptik.app/getHdLink.php?token={soup.find("button").get("data-tokenhd")}"
                        async with session.get(hd_url) as response:
                            data=await response.json()
                            FullReponse['hd'] = {}
                            FullReponse['hd'] = data
                            Content_list.append(Content(ContentTypes.Video, data['url']))

                    Caption=html.unescape(str(soup.find("div", class_="video-title").text))
                    users = re.findall(r'@\w+', Caption)
                    hashtags = re.findall(r'#\w+', Caption)

                    data_ = init.init(FullReponse, TiktokType, Content_list, ExtraOptions=init.init.Additionally(Caption=Caption, Users=users, Hashtags=hashtags))



    except: pass
    else: status=True
    return init.response(status, "SnapTik", data_)


