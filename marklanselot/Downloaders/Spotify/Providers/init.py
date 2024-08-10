from typing import List
from ... import Content

class init:
    class Additionally:
        def __init__(self, Duration: int=None, Artists: str=None, AlbumTitle: str=None, Date: str=None):
            self.Duration = Duration
            self.Artists = Artists
            self.AlbumTitle = AlbumTitle
            self.Date = Date


    def __init__(self, FullReponse, SongName: str, Content: List[Content.init], ExtraOptions: Additionally):
        self.FullReponse = FullReponse
        self.SongName = SongName
        self.Content = Content
        self.ExtraOptions = ExtraOptions


class response:
    def __init__(self, status: bool, service_name: str, data: init):
        self.status = status
        self.data = data
        self.service_name = service_name