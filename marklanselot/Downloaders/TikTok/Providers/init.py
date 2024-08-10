from typing import List
from ... import Content

class TiktokType:
    Photos = 'Photos'
    Video = 'Video'

class init:
    class Additionally:
        def __init__(self, Caption: str=None, Users: List[str]=None, Hashtags: List[str]=None, Preview: Content.init=None):
            self.Caption = Caption
            self.Users = Users
            self.Hashtags = Hashtags
            self.Preview = Preview


    def __init__(self, FullReponse, TiktokType: TiktokType, Content: List[Content.init], ExtraOptions: Additionally=None):
        self.FullReponse = FullReponse
        self.Content = Content
        self.TiktokType = TiktokType
        self.ExtraOptions = ExtraOptions


class response:
    def __init__(self, status: bool, service_name: str, data: init):
        self.status = status
        self.data = data
        self.service_name = service_name