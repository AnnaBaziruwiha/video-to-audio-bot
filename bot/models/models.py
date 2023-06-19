from dataclasses import dataclass

from utils.enums import Format


@dataclass
class Podcast:
    """Class representing a single piece of video/audio data"""

    title: str
    video_url: str
    local_file_path: str
    format: str
    duration: int
    size: int
    created_at: str
