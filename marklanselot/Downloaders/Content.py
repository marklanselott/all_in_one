from typing import List


class Types:
    Audio = 'Audio'
    Video = 'Video'
    Photo = 'Photo'
    Document = 'Document'


class init:
    def __init__(self, Type: Types, Url: str):
        self.Type = Type
        self.Url = Url

# Content: List[Content]