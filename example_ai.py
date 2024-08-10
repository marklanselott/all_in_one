import marklanselot





async def main():
    chat = [
        {"role": "user", "content": "1 + 1 ="},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "что я сказал в прошлом сообщении"},
    ]

    result = await marklanselot.AI.Providers.Qudata(chat)
    print(result.ResponseText)



import asyncio
asyncio.run(main())