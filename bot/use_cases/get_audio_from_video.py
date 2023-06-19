from models.models import Podcast
from adapters.video_downloaders import VideoDownloader
from adapters.video_to_audio_converters import AudioConverter


class GetAudioFromVideo:
    """
    This class encapsulates the process of obtaining audio from a video source.

    It associates a Podcast object with a VideoDownloader and an AudioConverter to facilitate
    the extraction of audio from a specified video source. This is achieved through the
    `get_audio_from_video` method which coordinates downloading the video and converting
    it to an audio format, then associating this audio with the provided Podcast object.
    """

    def __init__(
        self,
        podcast: Podcast,
        video_downloader: VideoDownloader,
        audio_converter: AudioConverter,
    ):
        self.podcast = podcast
        self.video_downloader = video_downloader
        self.audio_converter = audio_converter

    def get_audio_from_video(self):
        # Get url from the Podcast object
        # Find what downloader to use
        # Download the audio
        # Save the audio to the Podcast object
        ...
