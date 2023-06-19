from models.models import Podcast


class VideoDownloader:
    """
    VideoDownloader serves as an abstract base class to derive classes
    for downloading videos from different sources.

    An instance of this class holds a reference to a Podcast object and the desired save file type.
    It provides a download method, which when implemented in a derived class,
    should handle the process of downloading a video from the Podcast's URL and return
    the path of the downloaded video file.
    The download method raises NotImplementedError in the base class
    and must be overridden in any concrete subclass.
    """

    def __init__(self, podcast: Podcast, save_file_type: str) -> None:
        self.podcast = podcast
        self.save_file_type = save_file_type

    def download(self) -> str:
        """
        The function used to download the video
        Returns:
        The path of the downloaded video
        """
        raise NotImplementedError
