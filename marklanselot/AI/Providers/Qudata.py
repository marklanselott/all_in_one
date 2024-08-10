import asyncio, aiohttp, uuid
from typing import List
from .init import init

def CreateChat () -> dict:
    return {"message": "","dialogid": str(uuid.uuid4()),"userid": str(uuid.uuid4())}
    
def convert_chat(messages: List[dict], chat: dict):
    data = {}
    num_msg = 0
    for msg in messages:
        print(msg)
        data[f'dialogs[{num_msg}][role]'] = {}
        data[f'dialogs[{num_msg}][role]'] = msg['role']
        data[f'dialogs[{num_msg}][content]'] = {}
        data[f'dialogs[{num_msg}][content]'] = msg['content']
        chat['message'] = msg['content']
        num_msg += 1

    for i in chat:
        data[i] = {}
        data[i] = chat[i]
    
    return data

async def main(chat: List[dict]) -> init:
    status = False
    messages = chat
    ResponseText = ""
    try:
        async with aiohttp.ClientSession() as session:
            chat = CreateChat()
            data = convert_chat(messages, chat)
            async with session.post("https://qudata.com/ru/includes/sendmail/chat.php", data=data) as response:
                ResponseText = await response.text()
                messages.append({"role": "assistant", "content": ResponseText})
    
    except: pass
    else: status = True
    return init(status, "Qudata", messages, ResponseText)