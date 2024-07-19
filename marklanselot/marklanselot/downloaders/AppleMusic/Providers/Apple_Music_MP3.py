import aiohttp

need_for_selenium = False
home_page = 'https://apple-music-downloader.com/'

async def main(track_url: str) -> dict:
    result = {
        "get_track": None,
        "create_task": None,
        "generate_download_link": None,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"https://api.fabdl.com/apple-music/get?url={track_url}") as response:
            data = await response.json()
            result['get_track'] = data
            async with session.get(url=f"https://api.fabdl.com/apple-music/mp3-convert-task/{data['result']['gid']}/{data['result']['id']}") as response:
                data = await response.json()
                result['create_task'] = data
            while True:
                async with session.get(url=f"https://api.fabdl.com/apple-music/mp3-convert-progress/{data['result']['tid']}/{data['result']['track_id']}") as response:
                    if data['result']['status'] == 3:
                        data['result']['download_url'] = f"https://api.fabdl.com{data['result']['download_url']}"
                        result["generate_download_link"] = data
                        break
    return result