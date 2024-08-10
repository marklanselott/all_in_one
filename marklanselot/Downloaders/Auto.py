from . import AppleMusic, Spotify, Yt_music, TikTok

class Services:
    class apple_music:
        url = "https://music.apple.com"
        name = "AppleMusic"
        type = AppleMusic
    
    class spotify:
        url = "https://open.spotify.com/track"
        name = "Spotify"
        type = Spotify
    
    class yt_music:
        url = "https://music.youtube.com/watch?v="
        name = "YouTube Music"
        type = Yt_music

    class tiktok:
        url = "tiktok.com"
        name = "TikTok"
        type = TikTok

AppleMusic_url = "https://music.apple.com"
Spotify_url = "https://open.spotify.com/track"
Yt_music_url = "https://music.youtube.com/watch?v="
TikTok_url = "tiktok.com"

async def main(url: str):
    service = None

    if Services.apple_music.url in url:
        service = Services.apple_music
    elif Services.spotify.url in url:
        service = Services.spotify
    elif Services.yt_music.url in url:
        service = Services.yt_music
    elif Services.tiktok.url in url:
        service = Services.tiktok

    return service
