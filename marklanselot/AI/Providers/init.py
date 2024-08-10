from typing import List

class init:
    def __init__(self, status:  bool,  ModelName: str, Chat: List[dict], ResponseText: str) -> None:
        self.status = status
        self.ModelName = ModelName
        self.Chat = Chat
        self.ResponseText = ResponseText