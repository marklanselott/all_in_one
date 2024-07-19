import aiohttp

need_for_selenium = False
home_page = 'https://aaplmusicdownloader.com/'

async def main(track_url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"https://aaplmusicdownloader.com/api/applesearch.php?url={track_url}") as response:
            data = await response.json()
            async with session.post("https://aaplmusicdownloader.com/api/composer/swd.php", data={"song_name": data['name'], "artist_name": data['artist'], "url": track_url}) as response:
                return await response.json()
