from unittest.mock import Mock, patch
import pytest
from bot.converter import AudioConverter


@patch("bot.converter.AudioSegment")
def test_convert_to_mp3(mocked_AudioSegment):
    audio_path = "mock_audio_path"
    converter = AudioConverter()

    with patch(
        "os.path.getsize", return_value=51 * 1024 * 1024
    ):  # simulate a file larger than 50MB
        output_files = converter.convert_to_mp3(audio_path)

    assert len(output_files) > 1  # check that the audio file was split into chunks
    assert all(
        isinstance(path, str) for path in output_files
    )  # check that all paths are strings

    with patch(
        "os.path.getsize", return_value=49 * 1024 * 1024
    ):  # simulate a file smaller than 50MB
        output_files = converter.convert_to_mp3(audio_path)

    assert len(output_files) == 1  # check that the audio file was not split
