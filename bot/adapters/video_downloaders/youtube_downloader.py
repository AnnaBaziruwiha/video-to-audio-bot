from youtube_dl import YoutubeDL

from .base import VideoDownloader


class YouTubeDownloader(VideoDownloader):
    """A class that downloads the video from Youtube"""

    def download(self, url: str) -> str:
        """Downloads video and saves it as mp3"""
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "prefer_ffmpeg": True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            file_name = ydl.prepare_filename(info)
            file_name = file_name.rsplit(".", 1)[0] + ".mp3"
            ydl.download([url])
            return file_name
