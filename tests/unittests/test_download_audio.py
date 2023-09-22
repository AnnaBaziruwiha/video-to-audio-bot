import pytest


def test_download_audio_valid_url(bot_instance, mocker):
    # Mocking to avoid actual download
    mocker.patch(
        "youtube_dl.YoutubeDL.extract_info", return_value={"title": "Test Title"}
    )
    mocker.patch("youtube_dl.YoutubeDL.download")

    url = "http://www.youtube.com/watch?v=TestVideoID"
    output_path = bot_instance.download_audio(url=url)

    assert output_path is not None, f"Expected a file path, but got {output_path}"


def test_download_audio_invalid_url(bot_instance, mocker):
    mocker.patch(
        "youtube_dl.YoutubeDL.extract_info", side_effect=Exception("Invalid URL")
    )

    url = "http://www.invalidurl.com"
    with pytest.raises(Exception, match="Invalid URL"):
        bot_instance.download_audio(url=url)
