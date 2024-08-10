import marklanselot





async def main():
    result = await marklanselot.Downloaders.Yt_music.first_response("https://music.youtube.com/watch?v=GRuPHe2w1tg&si=aDyCnFnLzY0TFv2m")
    print(1)
    print(result.status)
    print()
    for i in result.data.Content:
        print(i.Type, i.Url)
        print()
    print()

    result = await marklanselot.Downloaders.AppleMusic.first_response("https://music.apple.com/ru/album/alive-in-you-feat-kim-walker-smith-live/1440832388?i=1440832533")
    print(2)
    print(result.status)
    print()
    for i in result.data.Content:
        print(i.Type, i.Url)
        print()
    print()

    result = await marklanselot.Downloaders.Spotify.first_response("https://open.spotify.com/track/7IZj7C9LM2jj0ISnyve3Ox?si=06293e9c75a24ef0")
    print(3)
    print(result.status)
    print()
    for i in result.data.Content:
        print(i.Type, i.Url)
        print()
    print()

    result = await marklanselot.Downloaders.TikTok.first_response("https://www.tiktok.com/@lisoviy_viktor_abrum/video/7398488070452022533?is_from_webapp=1&sender_device=pc")
    print(4)
    print(result.status)
    print()
    for i in result.data.Content:
        print(i.Type, i.Url)
        print()
    print()


    provider = await marklanselot.Downloaders.Auto("https://www.tiktok.com/@lisoviy_viktor_abrum/video/7398488070452022533?is_from_webapp=1&sender_device=pc")
    result = await provider.type.first_response("https://www.tiktok.com/@lisoviy_viktor_abrum/video/7398488070452022533?is_from_webapp=1&sender_device=pc")
    print(5)
    print(provider.name)
    print(result.status)
    print()
    for i in result.data.Content:
        print(i.Type, i.Url)
        print()
    print()




import asyncio
asyncio.run(main())