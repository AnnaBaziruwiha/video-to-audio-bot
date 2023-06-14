import re
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CallbackContext,
    CommandHandler,
)
from dotenv import load_dotenv
from .youtube import YouTubeDownloader
from .converter import AudioConverter
from .constants import WELCOME_MESSAGE, INVALID_INPUT_MESSAGE
from typing import Optional

load_dotenv()


class Bot:
    def __init__(
        self, token: str, downloader: YouTubeDownloader, converter: AudioConverter
    ):
        self.application = Application.builder().token(token).build()
        self.yt_downloader = downloader()
        self.converter = converter()

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
            filters.TEXT & (~filters.COMMAND), self.handle_message
        )
        self.application.add_handler(message_handler)
        self.application.add_handler(start_handler)
        self.application.run_polling(1.0)

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        """Processes the video from the link in the message and replies with an audio file"""
        message = update.message
        link = self.extract_youtube_link(message.text)
        if not self.is_youtube_link(link):
            await self.send_invalid_input_message(update, context)
            return
        audio_files = self.process_youtube_link(link)
        for file in audio_files:
            await self.send_audio(file, update, context)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="There you go!"
        )

    async def send_invalid_input_message(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Sends a message in response to an invalid request"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=INVALID_INPUT_MESSAGE
        )

    def extract_youtube_link(self, message: str) -> Optional[str]:
        """Extracts a YouTube link from a given message."""
        if "youtube.com" in message:
            return message.split(" ")[-1]
        return None

    def is_youtube_link(self, message: str) -> bool:
        """Checks whether a link is a youtube link or not"""
        youtube_regex = (
            r"(https?://)?(www\.)?"
            "(youtube|youtu|youtube-nocookie)\.(com|be)/"
            "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        )

        youtube_regex_match = re.match(youtube_regex, message)
        return youtube_regex_match is not None

    def process_youtube_link(self, youtube_link: str) -> str:
        """Processes the provided link and returns an audio file"""
        audio_stream = self.yt_downloader.download_audio(youtube_link)
        audio_file = self.converter.convert_to_mp3(audio_stream)
        return audio_file

    async def send_audio(
        self, audio_file: str, update: Update, context: CallbackContext
    ) -> None:
        """Sends an audio file"""
        await context.bot.send_audio(
            chat_id=update.effective_chat.id, audio=open(audio_file, "rb")
        )
