from bs4 import BeautifulSoup
import aiohttp

need_for_selenium = False
home_page = 'https://spotifymate.com/en'

async def main(track_url: str) -> str:
    data = {"url": track_url}

    home_url = "https://spotifymate.com/en"
    post_url = "https://spotifymate.com/action"

    async with aiohttp.ClientSession() as session:
        async with session.get(home_url) as response:
            html = await response.read()
            soup = BeautifulSoup(html, 'html.parser')

            hash = soup.find("form", class_ = "form-inline").find_all('input')[1]
            param = hash.get('name')
            value = hash.get('value')
            data[param] = value

            async with session.post(post_url, data=data) as response:
                return await response.text()



