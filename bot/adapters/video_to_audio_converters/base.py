from models.models import Podcast


class AudioConverter:
    """
    AudioConverter is an abstract base class designed to be the foundation
    for classes that convert video files into multiple audio files.

    Each instance of this class carries a Podcast object,
    a maximum size for audio files, and implements a convert_to_mp3 method.
    This method, when overridden in a concrete subclass,
    takes the path of a video file as input and returns the path of the resulting audio file.
    In the base class, the convert_to_mp3 method raises NotImplementedError
    and is intended to be implemented in derived classes.
    """

    def __init__(self, podcast: Podcast) -> None:
        self.podcast = podcast

    def convert_to_mp3(self, file_path: str) -> str:
        """Converts a video file into several audio files
        Args:
            file_path (str): Path to the video file
        Returns:
            str: Path to the audio file
        Raises:
            NotImplementedError: If the convert_to_mp3 method is not overridden in a concrete subclass.
        """
        raise NotImplementedError
