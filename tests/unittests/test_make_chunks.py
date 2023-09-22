import pytest
from pydub import AudioSegment


@pytest.mark.parametrize(
    "audio_length, chunk_length, expected_num_chunks",
    [
        (30000, 10000, 3),  # audio_length and chunk_length are in milliseconds
        (10000, 10000, 1),
    ],
)
def test_make_chunks(bot_instance, audio_length, chunk_length, expected_num_chunks):
    # Create an AudioSegment instance with a specific length
    audio = AudioSegment.silent(duration=audio_length)
    chunks = bot_instance._make_chunks(audio, chunk_length)
    assert (
        len(chunks) == expected_num_chunks
    ), f"Expected {expected_num_chunks} chunks, but got {len(chunks)}"
