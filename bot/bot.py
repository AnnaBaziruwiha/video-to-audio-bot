import asyncio
import logging
import os
import re
from typing import Any, List, Optional

import yt_dlp
from dotenv import load_dotenv
from pydub import AudioSegment
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)

from utils.constants import (
    INVALID_INPUT_MESSAGE,
    RESPONSE_MESSAGE,
    WAIT_MESSAGE,
    WELCOME_MESSAGE,
)

load_dotenv()

logger = logging.getLogger(__name__)


class Bot:
    """Handles the communication with the Telegram bot"""

    def __init__(self, token: str):
        self.token: str = token
        self.application: Application = Application.builder().token(self.token).build()

    async def send_welcome_message(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Sends a welcome message to the user"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=WELCOME_MESSAGE
        )

    def start(self) -> None:
        """Creates handlers for the bots, and starts polling"""
        start_handler = CommandHandler("start", self.send_welcome_message)
        message_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), self.handle_request
        )
        self.application.add_handler(message_handler)
        self.application.add_handler(start_handler)
        self.application.run_polling(1.0)

    def download_audio(self, url: str, output_directory: str = "downloads/") -> str:
        os.makedirs(output_directory, exist_ok=True)
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "outtmpl": os.path.join(output_directory, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            output_path = ydl.prepare_filename(info_dict)
            output_path = os.path.splitext(output_path)[0] + ".mp3"
            ydl.download([url])
            return output_path

    async def handle_request(self, update: Update, context: CallbackContext) -> None:
        """Function called when a user sends a message."""
        message = update.message
        if not message:
            return await self.return_invalid_input(update, context)
        url = self.extract_link(message.text)
        if not url:
            return await self.return_invalid_input(update, context)
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=WAIT_MESSAGE
            )
            path = self.download_audio(url=url)
            loop = asyncio.get_event_loop()
            splits = await loop.run_in_executor(None, self.split_audio, path)
            for split in splits:
                logger.info(f"Sending split {split}")
                with open(split, "rb") as audio_file:
                    await update.message.reply_audio(
                        audio_file, read_timeout=60, write_timeout=60
                    )
        except Exception as e:
            logger.exception(e)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Error: {e}"
            )
            return
        await self.return_success(update, context)

    def extract_link(self, message: str) -> Optional[str]:
        """Extracts the YouTube link from the message."""
        url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = re.findall(url_regex, message)
        for url in urls:
            if self._is_youtube_link(url):
                return url
        return None

    def _is_youtube_link(self, url: str) -> bool:
        """Returns True if it's a YouTube link"""
        youtube_regex = (
            r"(https?://)?(www\.)?"
            r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
            r"(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        )
        return re.match(youtube_regex, url) is not None

    @staticmethod
    def _make_chunks(audio: AudioSegment, chunk_length_ms: int) -> List[AudioSegment]:
        """Breaks large audio files into chunks"""
        return [
            audio[i : i + chunk_length_ms]
            for i in range(0, len(audio), chunk_length_ms)
        ]

    def split_audio(self, audio_path: str, max_size_mb: int = 50) -> List[Any]:
        """Splits audio into chunks if it exceeds max_size_mb"""
        audio = AudioSegment.from_file(audio_path)
        audio_size_mb = os.path.getsize(audio_path) / (1024 * 1024)

        if audio_size_mb <= max_size_mb:
            return [audio_path]

        chunk_length_ms = 10 * 60 * 1000
        chunks = self._make_chunks(audio, chunk_length_ms)

        output_files = []
        for i, chunk in enumerate(chunks):
            chunk_file_path = f"{audio_path.rsplit('.', 1)[0]}_part{i}.mp3"
            chunk.export(chunk_file_path, format="mp3")
            output_files.append(chunk_file_path)

        return output_files

    async def return_success(self, update: Update, context: CallbackContext) -> None:
        """Returns a success message to the user"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=RESPONSE_MESSAGE
        )

    async def return_invalid_input(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Sends a message in response to an invalid request"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=INVALID_INPUT_MESSAGE
        )
