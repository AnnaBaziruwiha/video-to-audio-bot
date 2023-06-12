import os
from typing import List
from pydub import AudioSegment
from .constants import MAX_AUDIO_SIZE


class AudioConverter:
    def __init__(self):
        self.max_file_size_mb = MAX_AUDIO_SIZE

    def convert_to_mp3(self, audio_path: str) -> List[str]:
        audio = AudioSegment.from_file(audio_path, format="mp3")
        audio_size_mb = os.path.getsize(audio_path) / (1024 * 1024)

        if audio_size_mb <= self.max_file_size_mb:
            # if the file size is less than or equal to 50 MB, no need to split
            return [audio_path]

        # if the file size is larger than 50 MB, need to split it
        chunk_length_ms = 10 * 60 * 1000  # length of each audio chunk, in milliseconds
        chunks = self._make_chunks(audio, chunk_length_ms)

        output_files = []
        for i, chunk in enumerate(chunks):
            chunk_file_path = f"{audio_path.rsplit('.', 1)[0]}_part{i}.mp3"
            chunk.export(chunk_file_path, format="mp3")
            output_files.append(chunk_file_path)

        os.remove(audio_path)  # remove the original large file

        return output_files  # return a list of file paths

    @staticmethod
    def _make_chunks(audio: AudioSegment, chunk_length_ms: int) -> List[AudioSegment]:
        return [
            audio[i : i + chunk_length_ms]
            for i in range(0, len(audio), chunk_length_ms)
        ]
