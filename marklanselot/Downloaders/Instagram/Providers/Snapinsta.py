import aiohttp, re, subprocess, os, uuid
from bs4 import BeautifulSoup

need_for_selenium = False
home_page = 'https://snapinsta.app/ru'
need_install_node = True


async def main(insta_url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://snapinsta.app/action2.php') as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            token = soup.find_all("input")
            print(token)
            async with session.post("https://snaptik.app/abc2.php", data={"url": insta_url, "lang": "ru", "token": token, "action": "post"}) as response:
                js_file = f'{uuid.uuid4().hex}.js'
                def remove_first_and_last_char(s):
                    if len(s) <= 2: return ''
                    return s[1:-1]

                with open(js_file, 'w') as file: file.write(await response.text())
                result = subprocess.run(['node', js_file], capture_output=True, text=True)
                os.remove(js_file)
                print(result.stderr)
                


