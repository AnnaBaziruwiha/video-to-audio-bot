import os

from pydub import AudioSegment


def test_split_audio_no_split_required(bot_instance, tmp_path):
    # Create a small audio file
    audio = AudioSegment.silent(duration=10000)  # 10 seconds of silence
    audio_path = tmp_path / "audio.mp3"
    audio.export(audio_path, format="mp3")

    splits = bot_instance.split_audio(
        str(audio_path), max_size_mb=1
    )  # assuming 1 MB is higher than the size of audio

    assert len(splits) == 1 and splits[0] == str(
        audio_path
    ), "Expected no split, but the audio was split"


def test_split_audio_split_required(bot_instance, tmp_path):
    # Create a large audio file
    audio = AudioSegment.silent(duration=2000000)  # around 33 minutes of silence
    audio_path = tmp_path / "audio.mp3"
    audio.export(audio_path, format="mp3")

    splits = bot_instance.split_audio(
        str(audio_path), max_size_mb=1
    )  # assuming 1 MB is less than the size of audio

    assert len(splits) > 1, "Expected the audio to be split, but got no split"
    for split in splits:
        assert os.path.exists(split), f"Expected {split} to exist, but it doesn't"
