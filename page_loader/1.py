from enum import Enum
from typing import NamedTuple


class ImgTag(NamedTuple):
    name = 'img'
    attr = 'src'
    message = 'images'


class LinkTag(NamedTuple):
    name = 'link'
    attr = 'href'
    message = 'links'


class ScriptTag(NamedTuple):
    name = 'script'
    attr = 'src'
    message = 'scripts'


class Tags(Enum):
    IMG = ImgTag
    SCRIPT = ScriptTag
    LINK = LinkTag


for i in Tags:
    print(i)
