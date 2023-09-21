import asyncio
import logging
import os
import re
from typing import Any, List, Optional

import youtube_dl
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
    WELCOME_MESSAGE,
    WAIT_MESSAGE,
)

load_dotenv()


class Bot:
    """Handles the communication with the Telegram bot"""

    def __init__(self):
        self.token: str = os.getenv("TELEGRAM_TOKEN", "")
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

    def download_audio(self, url: str, output_directory: str = "audio_files/") -> str:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(
                url, download=False
            )  # Extract info without downloading
            title = info_dict.get("title", None)  # Get video title

            if title:
                # Replace unwanted characters with an underscore
                title = re.sub(r'[\\/*?:"<>|]', "_", title)
                # Get the first 4 words of the title
                title_words = title.split()[:4]
                # Form the output file name from the first 4 words of the title
                filename = f"{'_'.join(title_words)}.mp3"
                output_path = os.path.join(
                    output_directory, filename
                )  # Form the complete output path

                # Update the output path in ydl options
                ydl.params["outtmpl"] = output_path

                # Download the video
                ydl.download([url])

                return output_path

    async def handle_request(self, update: Update, context: CallbackContext) -> None:
        """Function called when a user sends a message."""
        message = update.message
        if not message:
            return self.return_invalid_input(update, context)
        url = self.extract_link(message.text)
        if not url:
            return await self.return_invalid_input(update, context)
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=WAIT_MESSAGE
            )
            # download audio for this youtube video
            path = self.download_audio(url=url)
            loop = asyncio.get_event_loop()
            # Run split_audio in a different thread to avoid blocking the event loop
            splits = await loop.run_in_executor(None, self.split_audio, path)
            for split in splits:
                logging.info(f"Exporting split {split}")
                with open(split, "rb") as audio_file:
                    logging.info(f"Sending split {split}")
                    await update.message.reply_audio(
                        audio_file, read_timeout=60, write_timeout=60
                    )
        except Exception as e:
            logging.exception(e)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Error: {e}"
            )
            return
        await self.return_success(update, context)

    def extract_link(self, message: str) -> Optional[str]:
        """Extracts the youtube link from the message."""
        url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = re.findall(url_regex, message)
        for url in urls:
            if self._is_youtube_link(url):
                return url
        return None

    def _is_youtube_link(self, url: str) -> bool:
        """Returns True if it's a youtube link"""
        youtube_regex = (
            r"(https?://)?(www\.)?"
            "(youtube|youtu|youtube-nocookie)\.(com|be)/"
            "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        )

        youtube_regex_match = re.match(youtube_regex, url)
        return youtube_regex_match is not None

    @staticmethod
    def _make_chunks(audio: AudioSegment, chunk_length_ms: int) -> List[AudioSegment]:
        """Breaks large audio files into chunks"""
        return [
            audio[i : i + chunk_length_ms]
            for i in range(0, len(audio), chunk_length_ms)
        ]

    def split_audio(self, audio_path: str, max_size_mb: int = 50) -> List[Any]:
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)
        audio_size_mb = os.path.getsize(audio_path) / (1024 * 1024)

        if audio_size_mb <= max_size_mb:
            # if the file size is less than or equal to 50 MB, no need to split
            return [audio_path]

        # if the file size is larger than 50 MB, need to split it
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
        if not context or not update:
            print("Update or context missing.")
            return
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
