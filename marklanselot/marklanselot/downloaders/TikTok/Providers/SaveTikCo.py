import aiohttp

need_for_selenium = False
home_page = 'https://savetik.co/en2'

async def main(tiktok_url: str, headers: dict=None) -> dict:
    async with aiohttp.ClientSession() as session:
        data = { "q": tiktok_url, "lang": "en" }
        async with session.post("https://savetik.co/api/ajaxSearch", data=data, headers=headers) as response: 
            return await response.json()

