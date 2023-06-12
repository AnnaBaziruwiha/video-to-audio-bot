from unittest.mock import Mock, patch
import pytest
from bot.youtube import YouTubeDownloader


@patch("bot.youtube.YoutubeDL")
def test_download_audio(mocked_YoutubeDL):
    youtube_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    downloader = YouTubeDownloader()

    with patch("os.path.exists", return_value=True):
        audio_file = downloader.download_audio(youtube_link)

    assert isinstance(
        audio_file, str
    )  # check that the returned audio file path is a string
