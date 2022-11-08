from enum import Enum
from typing import NamedTuple
from typing import Literal


class ArgumentParser(NamedTuple):
    """Cli arguments. Url for download page, command to specify path to
    save directory"""
    url: Literal['url']
    save_directory_short: Literal['-o']
    save_directory_long: Literal['--output']


class RecordingData(NamedTuple):
    """Data for recording, path to save data"""
    data: str or bytes
    path_to_save_data: str


class ImgTag(NamedTuple):
    """Basic information required for parsing the IMG tag"""
    name = 'img'
    attr = 'src'
    message = 'images'


class LinkTag(NamedTuple):
    """Basic information required for parsing the Link tag"""
    name = 'link'
    attr = 'href'
    message = 'links'


class ScriptTag(NamedTuple):
    """Basic information required for parsing the Script tag"""
    name = 'script'
    attr = 'src'
    message = 'scripts'


class Tags(Enum):
    """A class for iterating basic tags"""
    IMG = ImgTag
    SCRIPT = ScriptTag
    LINK = LinkTag
