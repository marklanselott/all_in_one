import aiohttp

need_for_selenium = False
home_page = 'https://spotifydown.com/ru'

headers = {
    ":authority": "api.spotifydown.com",
    ":method": "GET",
    ":path": "/metadata/track/73j8vyZoKX1V8wapDOobPW",
    ":scheme": "https",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,ru;q=0.5",
    "If-None-Match": 'W/"f2-YauKlO8/ZyN2SXvfDAneeeQZZc4"',
    "Origin": "https://spotifydown.com",
    "Priority": "u=1, i",
    "Referer": "https://spotifydown.com/",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

async def main(track_url: str) -> dict:
    id = track_url.split("/")[len(track_url.split("/"))-1].split("?")[0]

    song_info = {}
    song_link = {}

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.spotifydown.com/metadata/track/{id}', headers=headers) as response:
            song_info = await response.json()

        async with session.get(f'https://api.spotifydown.com/download/{id}', headers=headers) as response:
            song_link = await response.json()

    return {"info": song_info, "link": song_link}
