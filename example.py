import marklanselot, asyncio

spotify_track_url = "https://open.spotify.com/track/3RoycW4yhd2HCsWmLR7xIi?si=5b696d8fe9aa4973"

apple_music_track_url = "https://music.apple.com/ru/album/as-i-am/3631486?i=3631404"


async def main():
    result = marklanselot.downloaders.AppleMusic.Providers.APL_MATE()

asyncio.run(main())