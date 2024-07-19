import aiohttp
from bs4 import BeautifulSoup

need_for_selenium = False
home_page = 'https://ssstik.io/en-1'

headers = {
    ':authority': 'ssstik.io',
    ':method': 'POST',
    ':path': '/abc?url=dl',
    ':scheme': 'https',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,ru;q=0.5',
    'Content-Length': '67',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_ga=GA1.1.1318747629.1720567785; __gads=ID=2f6cb63162a88a8f:T=1720567785:RT=1721250114:S=ALNI_MZ1EfJ4pliHh7ETY1OKl8Hz36Byvg; __gpi=UID=00000e78f4e694a3:T=1720567785:RT=1721250114:S=ALNI_MYdRc6OQlz57abHluebvYxZh-cd7g; __eoi=ID=a288c150ba4603c2:T=1720567785:RT=1721250114:S=AA-AfjZS7X-SEc5rtj0ykswlxnYW; FCNEC=%5B%5B%22AKsRol-uwv3PKOagDTicidHbKkp7VbRWB7jGxTX8Dg2UrfLPZGuaLEittVaDTMTAPsFk5OvcBDN8XHz-GVp_lySuS13Ys-y_fdjQHGvZiHlW3ZN2vvT1GnmEtnxDKq9qJWJcJsi7DHnzn2uHOuptVikzgbeHjQi5lA%3D%3D%22%5D%5D; _ga_ZSF3D6YSLC=GS1.1.1721250113.2.1.1721250342.0.0.0',
    'Hx-Current-Url': 'https://ssstik.io/how-to-download-tiktok-video-1',
    'Hx-Request': 'true',
    'Hx-Target': 'target',
    'Hx-Trigger': '_gcaptcha_pt',
    'Origin': 'https://ssstik.io',
    'Priority': 'u=1, i',
    'Referer': 'https://ssstik.io/how-to-download-tiktok-video-1',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

async def main(tiktok_url: str, headers: dict=headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url="https://ssstik.io/en") as response:
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
                return await response.text()

